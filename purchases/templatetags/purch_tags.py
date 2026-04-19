from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from wagtail.models import Page
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden

from django.http import HttpRequest
from django.template import loader
from django import template
# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
from purchases.models import Purchase, MyPurchases

register = template.Library()


def purchase_owner(request):
    objects = Purchase.objects.all()
    # products = Product.objects.all()
    user = request.user.is_authenticated
    for item in objects:
        if item.is_owner:
            return True
        else:
            return False



# start Test
# def purchase_owner(request):
#     user = request.user.is_authenticated
#     objects = Purchase.objects.get(complete=complete)
#     # return objects
#     # products = Product.objects.all()
#     if objects:
#         return True
#     else:
#         return False
# End Test



def product_name(request):
    objects = Purchase.objects.all()
    user = request.user.is_authenticated
    for item in objects:
        if item.is_owner:
            return item
            return True
        else:
            return False


def current_page(request):

    user = request.user.is_authenticated
    objects = Purchase.objects.all()
    current = request.path
    # test = objects.product.url
    for item in objects:
        if item.product.url == current:
            return True
        else:
            return False

# @login_required
# def product_ownership(request, product_id):
#     product = get_object_or_404(Product, product_id=product_id)
#
#     # Assuming your Product model has a ForeignKey field named 'owner'
#     if request.user == product.owner:
#         # return True
#         # User owns the product, render the page
#         return render(request, 'product_detail.html', {'product': product})
#     else:
#         # return False
#         # User does not own the product, return 403 Forbidden
#         return HttpResponseForbidden("You do not own this product.")


@login_required
def product_ownership(request):
    user = request.user.is_authenticated
    # product_id = request.session['product_id'] = product.id
    # product = get_object_or_404(Product, product_id=product_id)
    product = Product.objects.all().values_list('id', flat=True)
    # user_id = Product.objects.all().values_list('user.id', flat=True)
    # Assuming your Product model has a ForeignKey field named 'owner'
    # for item in product:
    # if request.user == item.user:
    if request.user:
        return product
        # User owns the product, render the page
        # return render(request, 'product.html', {'product': product})
    else:
        return False
        # User does not own the product, return 403 Forbidden
        # return HttpResponseForbidden("You do not own this product.")


def is_product_owner(request):
    user = request.user.is_authenticated
    # is_owner = Purchase.objects.values('is_owner').filter(user=user)
    is_owner = Purchase.objects.filter(user=user)
    return is_owner





@login_required
@register.simple_tag(takes_context=True)
def specific_purchase_data(context):
    request = context['request']
    # current_user = user
    # context['current_user'] = current_user
    # context['page_data'] = page_data(request)
    # context['object_user'] = object_user(request)
    # context['trigger'] = trigger(request)
    # context['not_owner'] = not_owner(request)
    # context['product_name'] = product_name(request)
    # context['prod_name'] = direct(request)
    # context['testing'] = Purchase.objects.filter(user=user).values_list('product_name', flat=True)
    # context['page_obj'] = page_data()
    # is_owner = Purchase.objects.get(is_owner=is_owner)
    # context['is_owner'] = is_owner
    # purchase_objects = Purchase.objects.filter()
    # my_objects = Purchase.objects.filter(user=request.user.is_authenticated)
    # context["current_page"] = current_page(request)
    context["current_page"] = current_page(request)
    context["purchase_owner"] = purchase_owner(request)
    context["product_name"] = product_name(request)
    context["is_product_owner"] = is_product_owner(request)

    user = request.user.is_authenticated
    # my_objects = Purchase.objects.filter(user=user, is_owner=True)
    my_objects = Purchase.objects.all()
    products = Product.objects.all()
    context['my_objects'] = my_objects
    # context['my_objects'] = my_objects
    context['products'] = products
    return context

# def download(request):
#     user = request.user.is_authenticated
#     purchases_to_display = []
#     items = Purchase.objects.all()
#     for item in items:
#         if page.id == item.product_id:
#             break
#     context = {
#         'products': purchases_to_display
#     }


# @register.simple_tag(takes_context=True)
# def object_user(context):
#     if request.user.is_anonymous():
#         obj_user = Purchase.objects.all()
#         return obj_user
#     else:
#         obj_user = Purchase.objects.filter(user=request.user)
#         return obj_user


# @register.simple_tag(takes_context=True)
# def is_true(context):
#     request = context['request']
#     user = request.user
#     product_user = Purchase.objects.filter(user=user)
#     page_user = Product.id
#     if product_user == user:
#         return True
#     else:
#         return False


# @register.simple_tag()
# def just_purchase_data():
#     # purchase_objects = Purchase.objects.all()
#     for obj in Purchase.objects.all():
#         print(obj.product_id)
#     purchase_objects = Purchase.objects.get(product_id='id')
#     # context["purchase_objects"] = purchase_objects
#     # return context


# for obj in purchase_objects:
#     if obj.product_id:
#         print("Oh Yeah!")
#     else:
#         print("WTF!")

# return
# return context


# for obj in purchase_objects:
#     owner = obj.user
#     page = obj.product_id
#     # break
#     # current_user = user.is_authenticated and user == obj.user
#     current_user = user.is_authenticated and user == owner
#     context['current_user'] = current_user
#     current_page = page
#     context['current_page'] = current_page
#     break

# return specific_purchase_data
# return context


# for obj in specific_objects:
#     user = request.user
#     page_id = obj.id
#     context["page_id"] = page_id
#     product_name = obj.product_name
#     context["product_name"] = product_name
#     current_user = user.is_authenticated and user == obj.user
#     # complete = obj.complete
#     # context["complete"] = complete
#
#     if current_user:
#         return True
#     else:
#         return False
# return specific_purchase_data()
# Access request attributes, e.g., request.user, request.path
# return request.user

# @register.simple_tag(takes_context=True)
# def specific_purchase_data():
#     user = request.user
#     specific_objects = Purchase.objects.all()
#     for obj in specific_objects:
#         # user = User
#         current_user = user.is_authenticated == obj.user
#         page_id = Page.id == obj.product_id
#         if current_user:
#             return True
#         else:
#             return False
#     return specific_purchase_data()


# @login_required
# @register.simple_tag()
# def my_view(request):
#     current_user = request.user
#     context = {'user': current_user}
#     return context


# @register.simple_tag(takes_context=True)
# def my_custom_tag(context, *args, **kwargs):
#     request = context['request']
#     my_objects = Purchase.objects.all()
#     context['my_objects'] = my_objects
#     # is_owner = Purchase.objects.filter(is_owner=True, user=request.user.id).exists()
#
#     # is_owner = Purchase.objects.filter(is_owner=True, user=request.user.id).exists()
#
#     # context['is_owner'] = is_owner
#     user = request.user
#     return f"Current user: {user.username if user.is_authenticated else 'Guest'}"

# @register.simple_tag()
# def get_context():
#     """Provide additional context information."""
#     context = super().get_context()
#     my_objects = Purchase.objects.all()
#     context['my_objects'] = my_objects
#     return context
