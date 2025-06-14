import stripe
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.utils import timezone
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
import json
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from wagtail.models import Page
from decouple import config
from products.models import Product
from .models import Purchase
from django.conf import settings

import os

STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default=None)
stripe.api_key = STRIPE_SECRET_KEY


# STRIPE_ENDPOINT_SECRET = 'whsec_bb33398794bcd6609c130bcd103175f1b9ff5c55f6824e77bcfeb0af295c4c2d'
STRIPE_ENDPOINT_SECRET = config('STRIPE_ENDPOINT_SECRET', default=None)
endpoint_secret = STRIPE_ENDPOINT_SECRET

BASE_ENDPOINT = 'http://127.0.0.1:8000'

MY_GLOBAL_VAR = 0

def change_global_var(new_value):
    global MY_GLOBAL_VAR
    MY_GLOBAL_VAR = new_value

@csrf_exempt
def purchase_start_view(request):
    if not request.method == "POST":
        return HttpResponseBadRequest("Needs to be POST")
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Needs to be User")



    product_name = request.POST.get("product_name")
    product_id = request.POST.get("product_id")
    stripe_price = request.POST.get("stripe_price")
    product_url = request.POST.get("product_url")


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
    purchase.purchase_id = purchase.id
    purchase.save()

    now = datetime.datetime.now()
    purchase_date = now.strftime("%b %d, %Y")
    formatted_now = now.strftime("%Y-%m-%d")
    invoice_number = f"{formatted_now}-{purchase_id}"

    success_path = reverse("purchases:success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"
    cancel_path = reverse("purchases:stopped")
    success_url = f"{BASE_ENDPOINT}{success_path}"
    cancel_url = f"{BASE_ENDPOINT}{cancel_path}"
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        metadata={"purchase_id": purchase_id, "product_name": product_name, "invoice_number": invoice_number, "purchase_date": purchase_date, "product_url": product_url},
        success_url=success_url,
        cancel_url=cancel_url
    )

    checkout_id = checkout_session.id
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.save()






    # session = stripe.checkout.Session.modify(
    #     checkout_session.id,
    #     metadata={"purchase_id": purchase_id}
    #     ),
    # metadata = session.purchase_id.metadata
    # print(metadata)
    # print(session.created)

    # return HttpResponseRedirect("/purchases/success")
    stripe_checkout_id = request.session['checkout_id'] = checkout_session.id
    request.session.save()
    print(stripe_checkout_id, 'start_view')
    return HttpResponseRedirect(checkout_session.url)


def purchase_success_view(request):
    purchase_id = request.session.get('purchase_id')
    checkout_id = request.session.get('checkout_id')
    session = stripe.checkout.Session.retrieve(
        checkout_id
    )
    # print(session)
    # print(session.customer_details.name, 'success_view')
    # customer_name = session.customer_details.name
    print(purchase_id, 'success_view')
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.complete = True
        purchase.is_owner = True
        purchase.save()
    # return HttpResponse(f"Finished {purchase_id}, {customer_name}")
    # return HttpResponse("Purchase Is Complete!")
    return render(request, 'purchases/success.html', {'session': session})



def purchase_stopped_view(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        product = purchase.product
        del request.session['purchase_id']
        return HttpResponseRedirect(product.get_absolute_url())
    return HttpResponse("Stopped")

def redirect_view(request):
    response = redirect(checkout_session.url)
    return response


@login_required
def user_purchases(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchase_date')
    return render(request, 'products/product.html', {'purchases': purchases})


def my_view(request, product_id):
    page_data = Purchase.objects.filter(slug=slug)
    context = {'page_data': page_data}
    return render(request, 'products/product.html', context)
