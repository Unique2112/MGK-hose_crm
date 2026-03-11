from django.core.mail import EmailMessage
from .models import HoseRecord
from datetime import date, timedelta
from decimal import Decimal

def get_report_html(start_date, report_type):
    """ሪፖርቱን በHTML ሰንጠረዥ መልክ የሚያዘጋጅ ተግባር"""
    today = date.today()
    # መረጃዎችን ከዳታቤዝ ማውጣት
    records = HoseRecord.objects.filter(date__range=[start_date, today])
    sold_items = records.filter(status='Sold')
    lost_items = records.filter(status='Lost Sale')

    # የገንዘብ ስሌቶች (VAT 15%)
    total_before_vat = sum(item.unit_price for item in sold_items)
    vat_amount = total_before_vat * Decimal('0.15')
    grand_total = total_before_vat + vat_amount

    # የHTML ሪፖርት መዋቅር
    html_content = f"""
    <html>
    <body style="font-family: sans-serif; color: #333; line-height: 1.6; padding: 20px;">
        <div style="text-align: center; border-bottom: 2px solid #d32f2f; padding-bottom: 10px;">
            <h2 style="color: #d32f2f; margin-bottom: 0;">MGK MAKONNEN ETHIOPIA PLC</h2>
            <h3 style="margin-top: 5px; color: #555;">{report_type} SALES REPORT</h3>
            <p style="font-size: 0.9em;">Period: {start_date} to {today}</p>
        </div>

        <table border="1" style="border-collapse: collapse; width: 100%; margin-top: 20px; font-size: 11px; text-align: center;">
            <thead>
                <tr style="background-color: #f2f2f2; font-weight: bold;">
                    <th style="padding: 8px;">Date</th>
                    <th style="padding: 8px;">Client Name</th>
                    <th style="padding: 8px;">Tin No</th>
                    <th style="padding: 8px;">FS No.</th>
                    <th style="padding: 8px;">Payment Method</th>
                    <th style="padding: 8px;">Amount before vat</th>
                </tr>
            </thead>
            <tbody>
    """

    for item in sold_items:
        tin = getattr(item, 'tin_no', '-') or "-"
        fs = getattr(item, 'fs_no', '-') or "-"
        pay = getattr(item, 'payment_method', 'Cash')

        html_content += f"""
            <tr>
                <td style="padding: 6px;">{item.date}</td>
                <td style="padding: 6px; text-align: left;">{item.company_name}</td>
                <td style="padding: 6px;">{tin}</td>
                <td style="padding: 6px;">{fs}</td>
                <td style="padding: 6px;">{pay}</td>
                <td style="padding: 6px; text-align: right;">{item.unit_price:,.2f}</td>
            </tr>
        """

    html_content += f"""
            </tbody>
            <tfoot style="font-weight: bold;">
                <tr>
                    <td colspan="5" style="text-align: right; padding: 8px;">Sub Total:</td>
                    <td style="text-align: right; padding: 8px;">{total_before_vat:,.2f}</td>
                </tr>
                <tr>
                    <td colspan="5" style="text-align: right; padding: 8px;">VAT (15%):</td>
                    <td style="text-align: right; padding: 8px;">{vat_amount:,.2f}</td>
                </tr>
                <tr style="background-color: #eee; font-size: 1.1em;">
                    <td colspan="5" style="text-align: right; padding: 8px;">Grand Total:</td>
                    <td style="text-align: right; padding: 8px; border-bottom: 3px double #000;">{grand_total:,.2f}</td>
                </tr>
            </tfoot>
        </table>

        <div style="margin-top: 40px;">
            <h3 style="color: #d32f2f; border-bottom: 2px solid #d32f2f; padding-bottom: 5px; font-size: 1.1em;">Lost Sales Summary</h3>
            <table border="1" style="border-collapse: collapse; width: 100%; font-size: 11px;">
                <thead>
                    <tr style="background-color: #fce4ec;">
                        <th style="padding: 8px;">Client Name</th>
                        <th style="padding: 8px;">Product</th>
                        <th style="padding: 8px;">Reason for Lost Sale</th>
                    </tr>
                </thead>
                <tbody>
    """

    for item in lost_items:
        html_content += f"""
                <tr>
                    <td style="padding: 6px;">{item.company_name}</td>
                    <td style="padding: 6px;">{item.hose_designation}</td>
                    <td style="padding: 6px;">{item.get_lost_reason_display()}</td>
                </tr>
        """

    # የተስተካከለ የፊርማ ክፍል (Prepared by:- CRM System እና Signature)
    html_content += """
                </tbody>
            </table>
        </div>

        <div style="margin-top: 80px; width: 100%;">
            <table style="width: 100%; border: none; font-weight: bold;">
                <tr>
                    <td style="border: none; width: 50%; padding: 0; vertical-align: bottom;">
                        Prepared by:- CRM System
                    </td>
                    <td style="border: none; width: 50%; text-align: right; padding: 0; vertical-align: bottom;">
                        Signature: _______________________
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
    return html_content

def send_detailed_email(subject, html_content):
    """ኢሜይሉን በHTML ፎርማት የሚልክ ተግባር"""
    email = EmailMessage(
        subject,
        html_content,
        'uniqueuna7@gmail.com',
        ['uniqueuna7@gmail.com'],
    )
    email.content_subtype = "html"
    email.send()

def send_daily_report():
    html = get_report_html(date.today(), "DAILY")
    send_detailed_email(f"Daily Sales Report - {date.today()}", html)
    print("ዕለታዊ ሪፖርቱ በተሳካ ሁኔታ ተልኳል!")

def send_weekly_report():
    start = date.today() - timedelta(days=7)
    html = get_report_html(start, "WEEKLY")
    send_detailed_email(f"Weekly Sales Report - {date.today()}", html)
    print("ሳምንታዊ ሪፖርቱ በተሳካ ሁኔታ ተልኳል!")

def send_monthly_report():
    start = date.today() - timedelta(days=30)
    html = get_report_html(start, "MONTHLY")
    send_detailed_email(f"Monthly Sales Report - {date.today()}", html)
    print("ወርሃዊ ሪፖርቱ በተሳካ ሁኔታ ተልኳል!")
    from .views import get_customer_by_tin
urlpatterns = [
    # ... ሌሎች መንገዶች
    path('get-customer-by-tin/', get_customer_by_tin, name='get_customer_by_tin'),
]