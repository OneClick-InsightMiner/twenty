from datetime import timedelta

from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from .models import Invoice, Purchase


def accounting_va_dashboard(request):
    """Display sales and purchases with month-over-month KPIs."""
    active_tab = request.GET.get("tab", "ventes")

    now = timezone.now()
    start_current_month = now.replace(day=1)
    end_previous_month = start_current_month - timedelta(days=1)
    start_previous_month = end_previous_month.replace(day=1)

    invoices = Invoice.objects.filter(date__gte=start_current_month)
    purchases = Purchase.objects.filter(date__gte=start_current_month)

    invoice_total = invoices.aggregate(total=Sum("amount"))["total"] or 0
    purchase_total = purchases.aggregate(total=Sum("amount"))["total"] or 0

    prev_invoice_total = (
        Invoice.objects.filter(date__range=(start_previous_month, end_previous_month))
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )
    prev_purchase_total = (
        Purchase.objects.filter(date__range=(start_previous_month, end_previous_month))
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )

    context = {
        "active_tab": active_tab,
        "invoices": invoices,
        "purchases": purchases,
        "kpis": {
            "invoice_total": invoice_total,
            "purchase_total": purchase_total,
            "invoice_mom": invoice_total - prev_invoice_total,
            "purchase_mom": purchase_total - prev_purchase_total,
        },
    }
    return render(request, "va_dashboard.html", context)
