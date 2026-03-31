import csv
import io
from decimal import Decimal
from rest_framework import generics, status, parsers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import Organization
from .models import Transaction, Upload
from .serializers import TransactionSerializer


def get_org(slug):
    return Organization.objects.get(slug=slug)


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['type', 'category', 'source', 'is_restricted']
    ordering_fields = ['date', 'amount', 'category']
    search_fields = ['description', 'vendor', 'note']

    def get_queryset(self):
        org = get_org(self.kwargs['slug'])
        qs = Transaction.objects.filter(organization=org)
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        return qs

    def perform_create(self, serializer):
        org = get_org(self.kwargs['slug'])
        serializer.save(organization=org)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        org = get_org(self.kwargs['slug'])
        return Transaction.objects.filter(organization=org)


class UploadCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def create(self, request, slug):
        org = get_org(slug)
        file = request.FILES.get('file')
        source_type = request.data.get('source_type', 'bank')

        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        upload = Upload.objects.create(organization=org, file=file, source_type=source_type)

        content = file.read().decode('utf-8')
        if source_type == 'venmo':
            transactions = parse_venmo(content, org)
        else:
            transactions = parse_bank(content, org)

        created = Transaction.objects.bulk_create(transactions, ignore_conflicts=True)

        return Response({
            'upload_id': upload.id,
            'transactions_imported': len(transactions),
            'source_type': source_type,
        }, status=status.HTTP_201_CREATED)


# ===== PARSERS =====

BANK_CATEGORIES = {
    'TEAMSNAP': ('Registration', 'TeamSnap'),
    'SURVEYMONK': ('Technology', 'SurveyMonkey'),
    'ATHLETES ALLEY': ('Uniforms', 'Athletes Alley'),
    'HARDWARE': ('Field & Facilities', 'Fair Haven Hardware'),
    'LOWES': ('Field & Facilities', "Lowe's"),
    'BEACON': ('Field & Facilities', 'Beacon Athletics'),
    'GODADDY': ('Technology', 'GoDaddy'),
    'VALS TAVERN': ('Food & Events', "Val's Tavern"),
    'BAGEL': ('Food & Events', 'BagelMasters'),
    'CELLAR': ('Food & Events', 'The Cellar'),
    'INSTACART': ('Food & Events', 'Instacart'),
    'TWO RIVERS': ('League Dues', 'Two Rivers Little League'),
    'LITTLE LEAGUE': ('League Dues', 'Two Rivers Little League'),
    'DICKS SPORTING': ('Equipment', "Dick's Sporting Goods"),
    'MONMOUTH STEREO': ('A/V Equipment', 'Monmouth Stereo'),
    'USPS': ('Administrative', 'USPS'),
    'STAPLES': ('Administrative', 'Staples'),
    'EVITE': ('Administrative', 'Evite'),
    'MASON': ('Field & Facilities', 'E.F. Mason'),
    'VENMO': ('Venmo Transfer', 'Venmo'),
    'OTCHEAP': ('Printing & Signage', 'OTCheap CustomPrints'),
    'CUSTOMPRINT': ('Printing & Signage', 'OTCheap CustomPrints'),
    'NAUVOO': ('Food & Events', 'Nauvoo Grill Club'),
    'CHECK': ('Check Payment', None),
    'BP ': ('Fuel', None),
}

VENMO_CATEGORIES = {
    'SUPER BOWL': 'Fundraising - Super Bowl Pool',
    'SB POOL': 'Fundraising - Super Bowl Pool',
    'SB BOX': 'Fundraising - Super Bowl Pool',
    'BOXES': 'Fundraising - Super Bowl Pool',
    'SQUARES': 'Fundraising - Super Bowl Pool',
    'MARCH MADNESS': 'Fundraising - March Madness',
    'NCAA': 'Fundraising - March Madness',
    'BRACKET': 'Fundraising - March Madness',
    'SPONSOR': 'Sponsorship',
    'BANNER': 'Sponsorship',
    'SLIDE': 'Merchandise',
    'MAGNET': 'Merchandise',
    'STICKER': 'Merchandise',
    'BLANKET': 'Merchandise',
    'CLINIC': 'Clinics',
    'COOPERSTOWN': 'Cooperstown',
    'SURVIVOR': 'Fundraising - Other',
    'KNOCKOUT': 'Fundraising - Other',
    'SIDELINE': 'Equipment Resale',
    'T-SHIRT': 'Merchandise',
}


def categorize_bank(desc):
    d = desc.upper()
    for pattern, (category, vendor) in BANK_CATEGORIES.items():
        if pattern in d:
            return category, vendor
    return 'Other', None


def categorize_venmo(note):
    n = (note or '').upper()
    for pattern, category in VENMO_CATEGORIES.items():
        if pattern in n:
            return category
    return 'Other'


def parse_bank(content, org):
    reader = csv.DictReader(io.StringIO(content))
    transactions = []
    for row in reader:
        debit = Decimal(row.get('Debit', '0').replace(',', '') or '0')
        credit = Decimal(row.get('Credit', '0').replace(',', '') or '0')
        amount = credit if credit > 0 else -debit
        if amount == 0:
            continue

        desc = row.get('Description', '').strip()
        category, vendor = categorize_bank(desc)

        transactions.append(Transaction(
            organization=org,
            source='bank',
            date=row.get('Date', ''),
            description=desc,
            amount=amount,
            type='credit' if amount > 0 else 'debit',
            category=category,
            vendor=vendor,
            raw_data=dict(row),
        ))
    return transactions


def parse_venmo(content, org):
    lines = content.split('\n')
    header_idx = next((i for i, l in enumerate(lines) if 'ID' in l and 'Datetime' in l and 'Type' in l), 1)
    csv_content = '\n'.join(lines[header_idx:])

    reader = csv.DictReader(io.StringIO(csv_content))
    transactions = []
    for row in reader:
        amount_str = (row.get('Amount (total)', '') or '').replace('$', '').replace(',', '').replace('+', '').strip()
        try:
            amount = Decimal(amount_str)
        except Exception:
            continue
        if amount == 0:
            continue

        from_user = row.get('From', '')
        to_user = row.get('To', '')
        note = row.get('Note', '')
        desc = f"{from_user} → {to_user}: {note}"
        category = categorize_venmo(note)

        transactions.append(Transaction(
            organization=org,
            source='venmo',
            date=(row.get('Datetime', '') or '')[:10],
            description=desc.strip(),
            amount=amount,
            type='credit' if amount > 0 else 'debit',
            category=category,
            vendor=to_user if amount < 0 else from_user,
            note=note,
            raw_data=dict(row),
        ))
    return transactions
