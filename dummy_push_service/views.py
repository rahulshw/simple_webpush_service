import json

from django.http import HttpResponseBadRequest, Http404, JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models.subscription import Subscription
from .models.website import Website


def index(request):
    if request.method == 'GET':
        context = dict(
            websites=Website.objects.all()
        )
        return render(request, "index.html", context)


def public_key_view(request: HttpRequest):
    if request.method == 'GET':
        """ serve public key of a website """
        website_domain = request.GET.get('domain', None)
        if website_domain:
            website = Website.objects.get(domain=website_domain)
            if website:
                response = dict(
                    domain=website.domain,
                    public_key=website.vapid_public_key
                )
                return JsonResponse(response)
            else:
                return Http404()
        else:
            return HttpResponseBadRequest(content=b"domain is a required query param.")


@csrf_exempt
def subscribe_view(request: HttpRequest):
    if request.method == 'POST':
        """ subscribe a user"""
        website_domain = request.GET.get('domain', None)
        subscription_data = json.loads(request.body)
        if website_domain and subscription_data:
            Subscription.create_subscription(website_domain, subscription_data)
            return JsonResponse(dict(message=f'added a subscription for website {website_domain}'))
        else:
            return HttpResponseBadRequest
    else:
        return HttpResponseBadRequest

@csrf_exempt
def push_notif_view(request: HttpRequest):
    if request.method == 'POST':
        """ trigger push notifications for a website """
        website_domain = request.GET.get('domain', None)
        data = json.loads(request.body)
        if website_domain and data:
            Website.trigger_push_notif_to_all_subscribers_of_a_website(website_domain, data)
            response = dict(status='triggered')
            return JsonResponse(response)
        else:
            return HttpResponseBadRequest


def dashboard_view(request: HttpRequest):
    if request.method == 'GET':
        """ shows all registered websites with an option to push notifications their subscribers """
        all_websites = Website.objects.all()
        context = dict(all_websites=all_websites)
        return render(request, 'dashboard.html', context)



