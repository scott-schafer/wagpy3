from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
import stripe
from wagtail.models import Page
from django.shortcuts import render
from decouple import config
from products.models import Product
from .models import Purchase
import random


STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default=None)
stripe.api_key = STRIPE_SECRET_KEY

BASE_ENDPOINT = 'http://127.0.0.1:8000'

# Create your views here.
def purchase_start_view(request):
    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()

    number = random.randint(0, 1)
    if number == 1:
        return HttpResponseRedirect("/purchases/success")

    product_name = request.POST.get("product_name")
    print(product_name)

    product_id = request.POST.get("product_id")
    print(product_id)

    purchase = Purchase.objects.create(user=request.user, product_name=product_name, product_id=product_id)

    request.session["purchase_id"] = purchase.id




    return HttpResponseRedirect("/purchases/stopped")
    # return HttpResponse("Purchase Start")

def purchase_success_view(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.complete = True
        purchase.is_owner = True
        purchase.save()

    return HttpResponse(f"Finished {purchase_id}")


def purchase_stopped_view(request):
    return HttpResponse("Stopped")


