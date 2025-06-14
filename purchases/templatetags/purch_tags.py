from django.db import models
from django.contrib.auth.models import User, AnonymousUser

from django.http import HttpRequest
from django.template import loader
from django import template
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wagtail.models import Page
from products.models import Product
from purchases.models import Purchase, MyPurchases

register = template.Library()

# def object_user(request: HttpRequest):
#     user = request.user
#     # user_object = Purchase.objects.filter(user=user, is_owner=True)
#     purchase = Purchase.objects.all().values()
#     # print(purchase)
#     # return purchase



# def page_data(request: HttpRequest):
#     user = request.user
#     my_objects = Purchase.objects.filter(user=user)
#     if user.is_authenticated:
#         for obj in my_objects:
#             product_data = obj.product_id
#             return product_data




# def trigger(request: HttpRequest):
#     user = request.user.is_authenticated
#     my_objects = Purchase.objects.filter(user=request.user.id)
#     if user:
#         for obj in my_objects:
#             if obj.product_id:
#                 return True
#             else:
#                 return False



# def product_name(request: HttpRequest):
#     user = request.user
#     my_objects = Purchase.objects.filter(user=user)
#     if user.is_authenticated:
#         my_obj = []
#         for obj in my_objects:
#             my_obj.append(obj.product_name)
#         # return my_obj
#             # for i in my_obj:
#             #     if i == obj.product_name:
#             #         return i
#
#             # return my_obj
#             return str(my_obj).replace('[','').replace(']','').replace(',','').replace("'", " ")



# def user_auth(request: HttpRequest):
#
#     user = request.user.is_authenticated
#     my_objects = Purchase.objects.filter(user=request.user.id, is_owner=True)
#     if user:
#         for obj in my_objects:
#             prod_obj = obj
#             return prod_obj
















# def testing(request):
#     # request = context['request']
#     mydata = Purchase.objects.filter('product_name').values_list('product_name', flat=True)
#     # template = loader.get_template('template.html')
#     context = {
#     'mymembers': mydata,
#     }

# def direct(request):
#     # user = request.user
#     user = request.user.is_authenticated
#     # page = Page.objects.defer('id').all()
#     # product = Product.objects.filter(product_name=product_name)
#     mydata = Purchase.objects.filter(user=user)
#     prod_name = []
#     # for obj in mydata:
#     #     prod_name.append(obj.product_name)
#     # # return prod_name
#     # return str(prod_name).replace('[', '').replace(']', '').replace(',', '').replace("'", " ")
#     context = {
#         mydata
#     }
#     # return (context, request)
#     return mydata

# def not_owner(request: HttpRequest):
#     user = request.user.is_authenticated
#     my_objects = Purchase.objects.filter(user=request.user.id)
#     data = []
#     if user:
#         for obj in my_objects:
#             data.append(obj.product_id)
#         return data
            # print(data)







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
    # is_owner = Purchase.objects.all()
    # context['is_owner'] = is_owner
    # purchase_objects = Purchase.objects.filter()
    # context["purchase_objects"] = purchase_objects
    # my_objects = Purchase.objects.all()

    user = request.user.is_authenticated
    my_objects = Purchase.objects.filter(user=request.user.id, is_owner=True)
    context['my_objects'] = my_objects
    return context



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
