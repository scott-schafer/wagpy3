from wagtail import blocks
from wagtail_flexible_forms.models import AbstractSessionFormSubmission
from wagtail_flexible_forms.models import AbstractSubmissionRevision

from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.blocks import ImageBlock
from wagtail_flexible_forms import blocks as wff_blocks
from wagtail.contrib.forms.models import FormSubmission
from wagtail_flexible_forms.models import StreamFormMixin

from wagtail.contrib.forms.models import AbstractEmailForm
# from wagtail.blocks import PageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.blocks import RichTextBlock

from app_blocks import app_blocks


class InfoBlock(blocks.StaticBlock):
    class Meta:
        group = 'Standalone Blocks'
        icon = 'doc-empty'
        template = 'blocks/info_block.html'
        admin_text = 'This is a content divider with extra information.'
        label = 'Information Block'


class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.RichTextBlock(
        features=['bold', 'italic', 'link', 'document-link'],
    )


class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(), **kwargs)

    class Meta:
        group = 'Iterable'
        icon = 'tasks'
        template = 'blocks/faq_list_block.html'
        label = 'Frequently Asked Questions'


class TextBlock(blocks.TextBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, help_text="Just a block of text.")

    class Meta:
        group = 'Standalone Blocks'
        icon = 'edit'
        template = 'blocks/text_block.html'


class CarouselBlock(blocks.StreamBlock):
    image = ImageChooserBlock()
    quotation = blocks.StructBlock([
        ('text', blocks.TextBlock()),
        ('author', blocks.TextBlock()),
    ])

    class Meta:
        group = 'Iterable'
        icon = 'copy'
        template = 'blocks/carousel_block.html'


class CallToActionBlock(blocks.StructBlock):
    text = blocks.RichTextBlock(
        features=['bold', 'italic'],
        required=True
    )
    page = blocks.PageChooserBlock()
    button_text = blocks.CharBlock(
        max_length=100,
        required=False,
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        page = value.get('page')
        button_text = value.get('button_text')
        context['button_copy'] = button_text if button_text else page.title
        return context

    class Meta:
        icon = 'link-external'
        template = 'blocks/call_to_action_block.html'
        label = 'Call To Action Block'


class ImageBlock(ImageChooserBlock):
    class Meta:
        group = 'Standalone Blocks'
        icon = 'image'
        template = 'blocks/image_block.html'


class ArticleSectionBlock(blocks.StructBlock):
    """A block for a single section with a header and content."""
    header = blocks.CharBlock(required=True)
    content = blocks.RichTextBlock(
        features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'document-link', 'image', 'ol', 'ul', 'blockquote',
                  'code'],
        required=False)

    class Meta:
        template = 'blocks/article_section_block.html'
        icon = 'title'


class NewsletterSignupBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, help_text="Title for the signup form")
    email_address = blocks.EmailBlock(required=True, help_text="Your email address")
    submit_button_text = blocks.CharBlock(default="Subscribe")

    class Meta:
        icon = "mail"
        template = "blocks/newsletter_signup_block.html"


class ContactInfoBlock(blocks.StructBlock):
    """A block for contact details, including an email field."""
    name = blocks.CharBlock(label="Your Name", required=True)
    email = blocks.EmailBlock(label="Your Email Address", required=True, help_text="Enter a valid email address.")
    message = blocks.TextBlock(label="Your Message", required=False)

    class Meta:
        icon = "mail"


# STREAMFORM_FIELDS = [
#     # Include form field blocks from wagtail_flexible_forms.
#     ("sf_singleline", wff_blocks.CharFieldBlock(group="Fields")),
#     ("sf_multiline", wff_blocks.TextFieldBlock(group="Fields")),
#     ("sf_checkboxes", wff_blocks.CheckboxesFieldBlock(group="Fields")),
#     ("sf_radios", wff_blocks.RadioButtonsFieldBlock(group="Fields")),
#     ("sf_dropdown", wff_blocks.DropdownFieldBlock(group="Fields")),
#     ("sf_checkbox", wff_blocks.CheckboxFieldBlock(group="Fields")),
#     ("sf_date", wff_blocks.DateFieldBlock(group="Fields")),
#     ("sf_time", wff_blocks.TimeFieldBlock(group="Fields")),
#     ("sf_datetime", wff_blocks.DateTimeFieldBlock(group="Fields")),
#     ("sf_image", wff_blocks.ImageFieldBlock(group="Fields")),
#     ("sf_file", wff_blocks.FileFieldBlock(group="Fields")),
#     # And content blocks from Wagtail!
#     ("text", blocks.RichTextBlock(group="Content")),
#     ("image", ImageBlock(group="Content")),
# ]


# from wagtail_flexible_forms.models import AbstractSessionFormSubmission
# from wagtail_flexible_forms.models import AbstractSubmissionRevision
#
#
# class MySubmissionRevision(AbstractSubmissionRevision):
#     pass
#
#
# class MySessionFormSubmission(AbstractSessionFormSubmission):
#     @staticmethod
#     def get_revision_class():
#         return MySubmissionRevision


# from wagtail.admin.panels import FieldPanel
# from wagtail.contrib.forms.models import FormSubmission
# from wagtail.fields import RichTextField
# from wagtail.fields import StreamField
# from wagtail.models import Page
# from wagtail_flexible_forms.models import StreamFormMixin


# class StreamFormPage(StreamFormMixin, Page):
#     template = "home/stream_form_page.html"
#     landing_page_template = "home/form_page_landing.html"
#
#     # Typical Wagtail field, like any other page.
#     intro = RichTextField(blank=True)
#
#     # Set ``form_fields`` to contain our Streamform fields.
#     form_fields = StreamField(STREAMFORM_FIELDS)
#
#     content_panels = Page.content_panels + [
#         FieldPanel("intro"),
#         FieldPanel("form_fields"),
#     ]
#
#     @staticmethod
#     def get_submission_class():
#         """
#         Submission class is used to store the final form
#         submission, after the user has finished their session.
#
#         For simplicity, use Wagtail's default FormSubmission class.
#         """
#         return FormSubmission
#
#     @staticmethod
#     def get_session_submission_class():
#         """
#         Session submission class is used to store temporary
#         data while the form is being filled out, i.e. for
#         multi-step forms.
#
#         You must return something that inherits from
#         ``AbstractSessionFormSubmission``.
#         """
#         return MySessionFormSubmission
