
from django.db import models
from datetime import date
import stripe
from wagtail.models import Page
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.panels import FieldPanel
from django.conf import settings
from decouple import config
from products.models import Product

class Purchase(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=1)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=120, null=True, help_text="This Name must match the product name Exactly!")
    purchase_id = models.CharField(max_length=120, null=True)
    purchase_invoice = models.CharField(max_length=120, null=True)
    stripe_checkout_session_id = models.CharField(max_length=220, null=True, blank=True)
    # handle = models.SlugField(unique=True, null=True)
    complete = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    stripe_price = models.IntegerField(default=0)
    timestamp = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.user} - {self.product_name}"

    def get_context(self, request, *args, **kwargs):
        """Adding products information to page"""
        context = super().get_context(request, *args, **kwargs)
        # context["product_model"] = Product.objects.all()
        # context["features_page"] = FeaturesPage.objects.live().public()
        # context["services_page"] = ServicesPage.objects.live().public()
        # context["products_page"] = ProductsPage.objects.live().public()
        # context["testimonials"] = Testimonial.objects.all()
        # context["faq_page"] = FaqPage.objects.live().public()
        return context




class Meta:
    verbose_name = "Purchase"
    verbose_name_plural = "Purchases"

    panels = [FieldPanel("user"), FieldPanel("product_id"), FieldPanel("product_name"), FieldPanel("purchase_id"), FieldPanel("complete"), FieldPanel("stripe_price"), FieldPanel("timestamp")]

class MyPurchases(Page):
    template = "purchases/my_purchases.html"
    # template = "products/product.html"

    def get_context(self, request, *args, **kwargs):
        """Provide additional context information."""
        context = super().get_context(request)
        # my_objects = Purchase.objects.all()
        # my_objects = Purchase.objects.all()
        my_objects = Purchase.objects.filter(user=request.user.id)
        context['my_objects'] = my_objects
        return context
