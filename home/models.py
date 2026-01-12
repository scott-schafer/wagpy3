from django.db import models

from wagtail.models import Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
# from wagtailcaptcha.models import WagtailCaptchaEmailForm
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel

FORM_FIELD_CHOICES = (
    ('singleline', ('Single line text')),
    ('multiline', ('Multi-line text')),
    ('email', ('Email')),
    ('url', ('URL')),
)


class CustomAbstractFormField(AbstractFormField):
    field_type = models.CharField(
        verbose_name="Field Type",
        max_length=16,
        choices=FORM_FIELD_CHOICES,
    )

    class Meta:
        abstract = True
        ordering = ["sort_order"]


class FormField(CustomAbstractFormField):
    page = ParentalKey(
        "HomePage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class HomePage(AbstractEmailForm, Page):
    template = "home/home_page.html"
    max_count = 1

    sub_title = models.CharField(max_length=255, blank=True, null=True)
    thank_you_text = RichTextField(
        blank="True"
    )

    content_panels = Page.content_panels + [
        FieldPanel("sub_title"),
        MultiFieldPanel([
            InlinePanel("form_fields", label="Form Fields"),
            FieldPanel("thank_you_text"),
            FieldPanel("from_address"),
            FieldPanel("to_address"),
            FieldPanel("subject"),
            ], heading="Email Form Information")
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding products information to page"""
        context = super().get_context(request, *args, **kwargs)
        # context['custom_data'] = 'This is a custom data'

        return context
