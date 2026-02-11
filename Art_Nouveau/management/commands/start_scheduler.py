# Art_Nouveau/management/commands/start_scheduler.py

import logging
from datetime import timedelta
import random

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mass_mail, mail_admins
from django.contrib.auth import get_user_model

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from Art_Nouveau.models import Discount, Product, UserProductView

logger = logging.getLogger('django')
User = get_user_model()


# --- TASK 1: Ștergere utilizatori neconfirmați ---
def delete_unconfirmed_users():
    """
    Șterge utilizatorii care nu au confirmat email-ul și au fost creați
    acum mai mult de K minute (pentru a le da un timp de grație).
    """
    # Timp de grație: Ștergem doar dacă au trecut K minute de la înregistrare
    # și tot nu au confirmat.
    time_threshold = timezone.now() - timedelta(minutes=settings.K_DELETE_UNCONFIRMED_MINUTES)

    users_to_delete = User.objects.filter(
        email_confirmed=False,
        date_joined__lt=time_threshold
    )

    count = users_to_delete.count()

    if count > 0:
        deleted_users_info = [f"{u.username} ({u.email})" for u in users_to_delete]
        users_to_delete.delete()
        logger.info(f"TASK EXECUTION: Deleted {count} unconfirmed users: {', '.join(deleted_users_info)}")
    else:
        logger.info("TASK EXECUTION: No unconfirmed users found to delete.")


# --- TASK 2: Newsletter Săptămânal ---
def send_weekly_newsletter():
    """
    Trimite un newsletter cu 3 produse recomandate (aleatorii) către userii vechi.
    """
    # 1. Selectare useri eligibili (mai vechi de X minute)
    time_limit = timezone.now() - timedelta(minutes=settings.X_USER_AGE_MINUTES)
    eligible_users = User.objects.filter(
        date_joined__lte=time_limit,
        email_confirmed=True,
        is_active=True
    )

    if not eligible_users.exists():
        logger.info("TASK EXECUTION: Newsletter skipped. No eligible users found.")
        return

    # 2. Generare conținut automat (3 produse random)
    products = list(Product.objects.filter(stock__gt=0))
    if len(products) >= 3:
        random_products = random.sample(products, 3)
    else:
        random_products = products

    product_text = "\n".join([f"- {p.name}: ${p.price}" for p in random_products])

    current_date = timezone.now().strftime("%d-%m-%Y")
    subject = f"Art Nouveau Weekly Digest - {current_date}"

    # Construirea listei de mesaje
    messages_to_send = []
    sender = 'newsletter@artnouveau.com'

    for user in eligible_users:
        # Mesaj personalizat (conținutul diferă ușor prin username)
        body = f"""Hello {user.username},

Here are our top picks for you this week:
{product_text}

Don't miss out on our art collection!

Best regards,
The Art Nouveau Team
"""
        messages_to_send.append((subject, body, sender, [user.email]))

    # Trimitere efectivă
    try:
        send_mass_mail(tuple(messages_to_send), fail_silently=False)
        logger.info(f"TASK EXECUTION: Weekly newsletter sent to {len(messages_to_send)} users.")
    except Exception as e:
        logger.error(f"TASK EXECUTION ERROR: Could not send newsletter: {e}")


# --- TASK 3 (Custom): Curățare Promoții Expirate ---
def cleanup_expired_discounts():
    """
    Șterge din baza de date codurile de reducere care au expirat.
    """
    now = timezone.now()
    expired = Discount.objects.filter(expiration_date__lt=now)
    count = expired.count()

    if count > 0:
        expired.delete()
        logger.info(f"TASK EXECUTION: Cleaned up {count} expired discount codes.")
    else:
        logger.info("TASK EXECUTION: No expired discounts found.")


# --- TASK 4 (Custom): Raport Săptămânal Admin ---
def send_admin_stats():
    """
    Trimite un email către admini cu statistici despre cele mai vizualizate produse.
    """
    # Luăm vizualizările din ultima săptămână
    last_week = timezone.now() - timedelta(days=7)
    recent_views = UserProductView.objects.filter(view_date__gte=last_week)

    total_views = recent_views.count()

    # Un mic raport simplu
    report = f"Weekly Admin Report ({timezone.now().date()})\n\n"
    report += f"Total Product Views: {total_views}\n"

    # Verificăm dacă există stocuri critice
    low_stock_products = Product.objects.filter(stock__lte=3)
    if low_stock_products.exists():
        report += "\nWARNING: The following products have LOW STOCK:\n"
        for p in low_stock_products:
            report += f"- {p.name} (Stock: {p.stock})\n"

    try:
        mail_admins("Weekly Site Statistics", report)
        logger.info("TASK EXECUTION: Admin stats email sent.")
    except Exception as e:
        logger.error(f"TASK EXECUTION ERROR: Could not send admin stats: {e}")


# --- COMANDA DE PORNIRE ---
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """Șterge log-urile de execuție mai vechi de o săptămână."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # 1. Configurare Task Ștergere Useri (Interval: K minute)
        scheduler.add_job(
            delete_unconfirmed_users,
            trigger=CronTrigger(minute=f"*/{settings.K_DELETE_UNCONFIRMED_MINUTES}"),
            id="delete_unconfirmed_users",
            max_instances=1,
            replace_existing=True,
            misfire_grace_time=600
        )
        print(f"Added job: delete_unconfirmed_users (Every {settings.K_DELETE_UNCONFIRMED_MINUTES} mins)")

        # 2. Configurare Task Newsletter (Cron: Ziua Z, Ora O)
        # apscheduler folosește primele 3 litere pt ziua săptămânii în engleză (mon, tue...)
        scheduler.add_job(
            send_weekly_newsletter,
            trigger=CronTrigger(
                day_of_week=settings.Z_NEWSLETTER_DAY,
                hour=settings.O_NEWSLETTER_HOUR,
                minute=0
            ),
            id="send_weekly_newsletter",
            max_instances=1,
            replace_existing=True,
            misfire_grace_time=600
        )
        print(
            f"Added job: send_weekly_newsletter (Every {settings.Z_NEWSLETTER_DAY} at {settings.O_NEWSLETTER_HOUR}:00)")

        # 3. Configurare Task Custom 1: Cleanup Discounts (Interval: M minute)
        scheduler.add_job(
            cleanup_expired_discounts,
            trigger=CronTrigger(minute=f"*/{settings.M_CHECK_DISCOUNTS_MINUTES}"),
            id="cleanup_expired_discounts",
            max_instances=1,
            replace_existing=True,
            misfire_grace_time=600
        )
        print(f"Added job: cleanup_expired_discounts (Every {settings.M_CHECK_DISCOUNTS_MINUTES} mins)")

        # 4. Configurare Task Custom 2: Raport Admin (Cron: Ziua Z2, Ora O2)
        scheduler.add_job(
            send_admin_stats,
            trigger=CronTrigger(
                day_of_week=settings.Z2_STATS_DAY,
                hour=settings.O2_STATS_HOUR,
                minute=0
            ),
            id="send_admin_stats",
            max_instances=1,
            replace_existing=True,
            misfire_grace_time=600
        )
        print(f"Added job: send_admin_stats (Every {settings.Z2_STATS_DAY} at {settings.O2_STATS_HOUR}:00)")

        # Task de mentenanță internă pentru scheduler (șterge log-urile vechi de execuție)
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        try:
            logger.info("Starting scheduler...")
            print("Scheduler started! Press Ctrl+C to exit.")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            print("Scheduler stopped successfully!")