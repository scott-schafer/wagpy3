from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
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
        features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'document-link', 'image', 'ol', 'ul', 'blockquote', 'code'],
        required=False)

    class Meta:
        template = 'blocks/article_section_block.html'
        icon = 'title'

