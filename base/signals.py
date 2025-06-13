from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User
import ssl
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        try:
            subject = 'Welcome to BookStore'
            message = f'''
            Hello {instance.full_name},

            Thank you for registering with BookStore!

            Best regards,
            BookStore Team
            '''
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [instance.email]
            
            # Create unverified SSL context
            ssl._create_default_https_context = ssl._create_unverified_context

            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
                connection=None,
            )
        except Exception as err:
            logger.exception(err)