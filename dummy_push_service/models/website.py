import uuid
from django.db import models

from ..utils import generate_vapid_key_pair


class Website(models.Model):
    domain = models.CharField(max_length=100, null=False)
    vapid_private_key = models.CharField(max_length=1000, null=False)
    vapid_public_key = models.CharField(max_length=1000, null=False)

    @classmethod
    def create_website(cls, domain: str):
        vapid_private_key, vapid_public_key = generate_vapid_key_pair()
        website = cls(domain=domain, vapid_private_key=vapid_private_key, vapid_public_key=vapid_public_key)
        website.save()

    @classmethod
    def trigger_push_notif_to_all_subscribers_of_a_website(cls, website_domain: str, data: dict):
        website = cls.objects.get(domain=website_domain)
        all_subscriptions_of_the_website = website.subscription_set.all()
        for subscription in all_subscriptions_of_the_website:
            try:
                subscription.trigger_push_notification(data)
            except Exception as e:
                print(f'error occurred while sending push notification for subscription id: {subscription.id}, '
                      f'error: {e}')
