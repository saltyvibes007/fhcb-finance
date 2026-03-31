from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import Organization
from transactions.models import Transaction


def get_org(slug):
    return Organization.objects.get(slug=slug)


class SummaryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        org = get_org(slug)
        txns = Transaction.objects.filter(organization=org)

        total_revenue = txns.filter(type='credit').aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = txns.filter(type='debit').aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'organization': org.name,
            'total_revenue': float(total_revenue),
            'total_expenses': float(abs(total_expenses)),
            'net_surplus': float(total_revenue + total_expenses),
            'transaction_count': txns.count(),
        })


class MonthlyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        org = get_org(slug)
        txns = Transaction.objects.filter(organization=org)

        monthly = txns.annotate(month=TruncMonth('date')).values('month').annotate(
            revenue=Sum('amount', filter=Q(type='credit')),
            expenses=Sum('amount', filter=Q(type='debit')),
            count=Count('id'),
        ).order_by('month')

        return Response([{
            'month': m['month'].isoformat()[:7],
            'revenue': float(m['revenue'] or 0),
            'expenses': float(abs(m['expenses'] or 0)),
            'net': float((m['revenue'] or 0) + (m['expenses'] or 0)),
            'transaction_count': m['count'],
        } for m in monthly])


class CategoriesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        org = get_org(slug)
        txns = Transaction.objects.filter(organization=org)

        categories = txns.values('category').annotate(
            revenue=Sum('amount', filter=Q(type='credit')),
            expenses=Sum('amount', filter=Q(type='debit')),
            count=Count('id'),
        ).order_by('-count')

        return Response([{
            'category': c['category'] or 'Uncategorized',
            'revenue': float(c['revenue'] or 0),
            'expenses': float(abs(c['expenses'] or 0)),
            'transaction_count': c['count'],
        } for c in categories])
