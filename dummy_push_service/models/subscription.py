import uuid
import json
from django.db import models
from .website import Website

from pywebpush import webpush


class Subscription(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, null=False)
    subscription_data = models.JSONField(null=False)

    def trigger_push_notification(self, data):
        return webpush(self.subscription_data, json.dumps(data),
                       vapid_private_key=self.website.vapid_private_key,
                       vapid_claims=dict(sub='mailto:rahul.shaw.2009@gmail.com'))

    @classmethod
    def create_subscription(cls, website_domain, subscription_data):
        website = Website.objects.get(domain=website_domain)
        subscription = Subscription(website=website, subscription_data=subscription_data)
        subscription.save()