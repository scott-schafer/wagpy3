from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.documents.models import Document, AbstractDocument
from wagtail.documents import get_document_model
from decouple import config
import pathlib
import stripe
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default=None)
stripe.api_key = STRIPE_SECRET_KEY

class ProductListingPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['products.Product']
    max_count = 1
    sub_title = models.CharField(max_length=255, blank=True, null=True, help_text="255 Characters max")
    sub_title_text = models.CharField(max_length=500, blank=True, null=True, help_text="500 Characters max")

    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
        FieldPanel('sub_title_text'),
    ]

    @property
    def get_child_pages(self):
        return self.get_children().public().live()

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        context["products"] = Product.objects.all()
        return context



class Product(Page):
    parent_page_types = ['products.ProductListingPage']
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        default=1,
    )
    product_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL)
    stripe_product_id = models.CharField(max_length=220, null=True, blank=True)
    product_name = models.CharField(max_length=120, help_text="The Purchase Product Name must match this name Exactly!")
    price = models.DecimalField(decimal_places=2, max_digits=10, default=9.99)
    og_price = models.DecimalField(decimal_places=2, max_digits=10, default=9.99)
    price_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    stripe_price_id = models.CharField(max_length=220, null=True, blank=True)
    stripe_price = models.IntegerField(default=999)  # 100 * price
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_owner = models.BooleanField(default=False)

    product_attachment = StreamField([
        ('document', DocumentChooserBlock()),
    ], null=True, blank=True)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return context

    def __str__(self):
        return self.product_name

    @property
    def display_price(self):
        return self.price

    def save(self, *args, **kwargs):
        if self.product_name:
            stripe_product_r = stripe.Product.create(name=self.product_name)
            self.stripe_product_id = stripe_product_r.id
        if not self.stripe_product_id:
            stripe_price_obj = stripe.Price.create(
                product=self.stripe_product_id,
                unit_amount=self.stripe_price,
                currency="usd"
            )
            self.stripe_price_id = stripe_price_obj.id

        if self.price != self.og_price:
            # price change
            self.og_price = self.price
            # trigger api call from stripe
            self.stripe_price = int(self.price * 100)
            if self.stripe_product_id:
                stripe_price_obj = stripe.Price.create(
                    product=self.stripe_product_id,
                    unit_amount=self.stripe_price,
                    currency="usd"
                )
                self.stripe_price_id = stripe_price_obj.id

            self.price_changed_timestamp = timezone.now()
        super().save(*args, **kwargs)


    content_panels = Page.content_panels + [
        FieldPanel("product_name"),
        FieldPanel("is_owner"),
        FieldPanel("price"),
        FieldPanel("og_price"),
        FieldPanel("stripe_product_id"),
        FieldPanel("stripe_price_id"),
        FieldPanel("stripe_price"),
        FieldPanel("product_image"),
        FieldPanel("product_attachment"),


    ]

class CustomDocument(AbstractDocument):
    # Custom field example:
    source = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    is_owner = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    admin_form_fields = Document.admin_form_fields + (
        # Add all custom fields names to make them appear in the form:
        'source',
        'is_owner',
        'is_free',
        'is_active',
    )
