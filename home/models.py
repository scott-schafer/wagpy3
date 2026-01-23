from django.db import models

from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from wagtail_flexible_forms import blocks as wff_blocks
from wagtail_flexible_forms.models import AbstractSessionFormSubmission
from wagtail_flexible_forms.models import AbstractSubmissionRevision
from wagtail.models import Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
# from wagtailcaptcha.models import WagtailCaptchaEmailForm
from modelcluster.fields import ParentalKey
from wagtail.fields import StreamField
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import FormSubmission
from wagtail_flexible_forms.models import StreamFormMixin
from wagtail.snippets.models import register_snippet
from app_blocks import app_blocks


FORM_FIELD_CHOICES = (
    ('singleline', ('Single line text')),
    ('multiline', ('Multi-line text')),
    ('email', ('Email')),
    ('url', ('URL')),
)


class CustomAbstractFormField(AbstractFormField):
    field_type = models.CharField(
        verbose_name="Field Type",
        blank=True,
        null=True,
        max_length=16,
        choices=FORM_FIELD_CHOICES,
    )

    class Meta:
        abstract = True
        ordering = ["sort_order"]


class FormField(CustomAbstractFormField):
    page = ParentalKey(
        "HomePage",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="form_fields",
    )

# class FormPage(AbstractEmailForm):
#     intro = RichTextField(blank=True)
#     thank_you_text = RichTextField(blank=True)
#
#     content_panels = AbstractEmailForm.content_panels + [
#         FieldPanel('intro'),
#         FieldPanel('thank_you_text'),
#         MultiFieldPanel([
#             InlinePanel("my_form_fields", label="Form Fields"),
#             FieldPanel("thank_you_text"),
#             FieldPanel("from_address"),
#             FieldPanel("to_address"),
#             FieldPanel("subject"),
#         ], heading="Email Form Information"),
#     ]


# class FormField(CustomAbstractFormField):
#     page = ParentalKey(
#         "FormPage",
#         blank=True,
#         null=True,
#         on_delete=models.CASCADE,
#         related_name="my_form_fields",
#     )


class HomePage(AbstractEmailForm):
    template = "home/home_page.html"
    max_count = 1

    sub_title = models.CharField(max_length=255, blank=True, null=True)
    thank_you_text = RichTextField(
        blank="True"
    )

    body = StreamField([
        # ('form_fields', app_blocks.StreamFormPage()),
    ], blank=True, null=True, )

    content_panels = Page.content_panels + [
        FieldPanel("sub_title"),
        FieldPanel("body"),
        MultiFieldPanel([
            InlinePanel("form_fields", label="Form Fields"),
            FieldPanel("thank_you_text"),
            FieldPanel("from_address"),
            FieldPanel("to_address"),
            FieldPanel("subject"),
        ], heading="Email Form Information"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding products information to page"""
        context = super().get_context(request, *args, **kwargs)
        # context['my_form_data'] = StreamFormField

        return context
