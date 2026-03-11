import os
import django
import sys

# የፕሮጀክቱን አቃፊ መንገድ ማዘጋጀት
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # 'core' የፕሮጀክትህ ስም ካልሆነ ቀይረው
django.setup()

from crm_app.utils import send_daily_report, send_weekly_report, send_monthly_report

if __name__ == "__main__":
    if len(sys.argv) > 1:
        report_type = sys.argv[1]
        
        if report_type == "daily":
            send_daily_report()
        elif report_type == "weekly":
            send_weekly_report()
        elif report_type == "monthly":
            send_monthly_report()
        else:
            print("እባክዎ ትክክለኛ የሪፖርት አይነት ያስገቡ (daily, weekly, monthly)")
    else:
        print("የሪፖርት አይነት አልተገለጸም!")