from django.conf import settings
from django.db.models import Sum, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from openai import OpenAI
from accounts.models import Organization
from transactions.models import Transaction


def get_org(slug):
    return Organization.objects.get(slug=slug)


class ChatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, slug):
        org = get_org(slug)
        messages = request.data.get('messages', [])

        if not settings.OPENAI_API_KEY:
            return Response({'error': 'OpenAI API key not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Build context from database
        txns = Transaction.objects.filter(organization=org)
        summary = txns.aggregate(
            total_revenue=Sum('amount', filter=Q(type='credit')),
            total_expenses=Sum('amount', filter=Q(type='debit')),
        )

        top_expenses = (
            txns.filter(type='debit', vendor__isnull=False)
            .values('vendor', 'category')
            .annotate(total=Sum('amount'))
            .order_by('total')[:10]
        )

        recent = txns.order_by('-date')[:50]

        revenue = float(summary['total_revenue'] or 0)
        expenses = float(abs(summary['total_expenses'] or 0))

        system_prompt = f"""You are an AI financial advisor for {org.name}. Here is the financial data:

Total Revenue: ${revenue:,.2f}
Total Expenses: ${expenses:,.2f}
Net: ${revenue - expenses:,.2f}
Transactions: {txns.count()}

Top Expenses by Vendor:
{chr(10).join(f"- {e['vendor'] or e['category']}: ${abs(float(e['total'])):,.2f}" for e in top_expenses)}

Recent transactions (last 50):
{chr(10).join(f"{t.date} | {t.type} | ${abs(float(t.amount)):,.2f} | {t.description[:60]} | {t.category or ''}" for t in recent)}

Answer concisely with real numbers. If you don't have the data, say so."""

        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{'role': 'system', 'content': system_prompt}] + messages,
                max_tokens=600,
                temperature=0.3,
            )
            reply = response.choices[0].message.content
            return Response({'reply': reply})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
