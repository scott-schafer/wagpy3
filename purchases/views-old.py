import stripe
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse
from wagtail.models import Page
from django.shortcuts import render
from decouple import config
from products.models import Product
from .models import Purchase
from django.conf import settings
# import random

STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default=None)
stripe.api_key = STRIPE_SECRET_KEY
STRIPE_ENDPOINT_SECRET = config('STRIPE_ENDPOINT_SECRET', default=None)
endpoint_secret = STRIPE_ENDPOINT_SECRET

BASE_ENDPOINT = 'http://127.0.0.1:8000'

webhook_endpoint = stripe.WebhookEndpoint.create(
  enabled_events=["charge.succeeded", "charge.failed"],
  url="https://example.com/my/webhook/endpoint",
)


@csrf_exempt
def purchase_start_view(request):
    if not request.method == "POST":
        return HttpResponseBadRequest("Needs to be POST")
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Needs to be User")



    product_name = request.POST.get("product_name")
    product_id = request.POST.get("product_id")
    stripe_price = request.POST.get("stripe_price")


    # purchase = Purchase.objects.create(user=request.user, product_name=product_name, product_id=product_id, stripe_price=stripe_price)
    # request.session['purchase_id'] = purchase.id



    stripe_product_obj = stripe.Product.create(name=product_name)
    stripe_product_id = stripe_product_obj.id

    stripe_price_obj = stripe.Price.create(
        product=stripe_product_id,
        unit_amount=stripe_price,
        currency="usd"
    )
    stripe_price_id = stripe_price_obj.id

    if stripe_price_id is None:
        return HttpResponseBadRequest("Stripe Processing Has Failed")
    # purchase = Purchase.objects.create(user=request.user, product=obj)
    # purchase = Purchase.objects.create(user=request.user, product_name=product_name, product_id=product_id)

    purchase = Purchase.objects.create(user=request.user, product_name=product_name, product_id=product_id, stripe_price=stripe_price)
    purchase_id = request.session['purchase_id'] = purchase.id
    # print(purchase_id)


    purchase.purchase_id = purchase.id
    purchase.save()

    success_path = reverse("purchases:success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"
    cancel_path = reverse("purchases:stopped")
    success_url = f"{BASE_ENDPOINT}{success_path}"
    cancel_url = f"{BASE_ENDPOINT}{cancel_path}"
    print(success_url, cancel_url)
    request.session['purchase_id'] = purchase.id

    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        metadata={"purchase_id": purchase_id},
        success_url=success_url,
        cancel_url=cancel_url
    )

    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.save()
    print(purchase_id)
    session = stripe.checkout.Session.modify(
        checkout_session.id,
        # metadata={"purchase_id": purchase_id}
        ),
    # metadata = session.purchase_id.metadata
    # print(metadata)
    # print(session)
    return HttpResponseRedirect(checkout_session.url, session)


# def view1(request):
#     request.session['purchase_id'] = purchase.id
#     return redirect(purchase_success_view)

    # return HttpResponse(f"Finished {purchase_id}")

# def purchase_success_view(request):
#     # purchase_id = request.session.get('purchase_id')
#     purchase_id = Purchase.objects.get(id=purchase_id)
#     print(purchase_id)
#     if purchase_id:
#         purchase = Purchase.objects.get(id=purchase_id)
#         purchase.completed = True
#         purchase.is_owner = True
#         purchase.save()
#         # del request.session['purchase_id']
#         # return HttpResponseRedirect(purchase.product.get_absolute_url())
#         # return HttpResponseRedirect(checkout_session.url)
#     # return HttpResponse(f"Finished {purchase_id}")
#     return HttpResponse("Purchase Is Complete!")

@csrf_exempt
def purchase_success_view(request):
    purchase_id = request.session.get('purchase_id')
    # purchase_id = request.session['purchase_id'] = purchase.id
    print(purchase_id)

    return HttpResponse(f"Finished {purchase_id}")

    # if purchase_id:
    #     purchase = Purchase.objects.get(id=purchase_id)
    #     purchase.completed = True
    #     purchase.save()
        # del request.session['purchase_id']
        # return HttpResponseRedirect(purchase.product.get_absolute_url())
    # return HttpResponse(f"Finished {purchase_id}")

@csrf_exempt
def purchase_stopped_view(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        product = purchase.product
        del request.session['purchase_id']
        return HttpResponseRedirect(product.get_absolute_url())
    return HttpResponse("Stopped")

import json
from django.http import HttpResponse

# Using Django
# @csrf_exempt
# def stripe_webhook(request):
#   stripe.api_key = config('STRIPE_SECRET_KEY', default=None)
#   payload = request.body
#   event = None
#
#   try:
#     event = stripe.Event.construct_from(
#       json.loads(payload), stripe.api_key
#     )
#   except ValueError as e:
#     # Invalid payload
#     return HttpResponse(status=400)
#
#   # Handle the event
#   if event.type == 'payment_intent.succeeded':
#     payment_intent = event.data.object # contains a stripe.PaymentIntent
#     # Then define and call a method to handle the successful payment intent.
#     # handle_payment_intent_succeeded(payment_intent)
#   elif event.type == 'payment_method.attached':
#     payment_method = event.data.object # contains a stripe.PaymentMethod
#     # Then define and call a method to handle the successful attachment of a PaymentMethod.
#     # handle_payment_method_attached(payment_method)
#   # ... handle other event types
#   else:
#     print('Unhandled event type {}'.format(event.type))
#
#   return HttpResponse(status=200)




# def stripe_webhook(request):
#     purchase.completed = True
#     purchase.is_owner = True
#     purchase.save()
#     return HttpResponse("Purchase Is Complete!")





@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = config('STRIPE_SECRET_KEY', default=None)
    stripe_endpoint_secret = "whsec_bb33398794bcd6609c130bcd103175f1b9ff5c55f6824e77bcfeb0af295c4c2d"
    # endpoint_secret = config('STRIPE_ENDPOINT_SECRET', default=None)
    print(endpoint_secret)
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print(payload)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_endpoint_secret
            # payload, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)



# Using Django
# @csrf_exempt
# def stripe_webhook(request):
#   payload = request.body
#   event = None
#
#   try:
#     event = stripe.Event.construct_from(
#       json.loads(payload), stripe.api_key
#     )
#   except ValueError as e:
#     # Invalid payload
#     return HttpResponse(status=400)
#
#   # Handle the event
#   if event.type == 'payment_intent.succeeded':
#     payment_intent = event.data.object # contains a stripe.PaymentIntent
#     # Then define and call a method to handle the successful payment intent.
#     # handle_payment_intent_succeeded(payment_intent)
#   elif event.type == 'payment_method.attached':
#     payment_method = event.data.object # contains a stripe.PaymentMethod
#     # Then define and call a method to handle the successful attachment of a PaymentMethod.
#     # handle_payment_method_attached(payment_method)
#   # ... handle other event types
#   else:
#     print('Unhandled event type {}'.format(event.type))
#
#   return HttpResponse(status=200)
