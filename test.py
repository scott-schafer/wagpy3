
To use BeautifulSoup in a Wagtail block, you first need to install it in your project's environment
. Then, create a custom StructBlock or RichTextBlock where you use Python code to import and process content with BeautifulSoup. This is especially useful for tasks like cleaning or parsing external HTML data before displaying it on your Wagtail site.



pip install beautifulsoup4 requests

Step 2: Create a custom blocks.py file
Inside one of your Wagtail apps (for example, a new blocks.py file within your home app), create a custom StructBlock. This block will contain the logic for processing the HTML input using BeautifulSoup


# blocks.py
from wagtail import blocks
from bs4 import BeautifulSoup

class HtmlProcessingBlock(blocks.StructBlock):
    """
    A custom block that takes raw HTML and processes it with BeautifulSoup.
    """
    raw_html = blocks.RichTextBlock(
        features=['h2', 'h3', 'bold', 'italic', 'link'],
        help_text='Enter the HTML content you want to process.'
    )

    class Meta:
        template = 'home/blocks/html_processing_block.html'
        icon = 'code'
        label = 'HTML Processor'


Step 3: Define the template for the block
Next, create the HTML template that will render your processed content. In the block's template, you can access the input from the editor as value.raw_html. Use Python to pass the processed content to the template



# templates/blocks/html_processing_block.html

{% load wagtailcore_tags %}
{% load static %}

<div class="html-processor-block">
    {% with html_content=value.raw_html %}
        {% if html_content %}
            {% comment %}
            Since you cannot run BeautifulSoup directly in a Django template,
            the processing logic must be done in a Python method.
            A simplified approach is to pass the value and let the template render it directly,
            but for more complex tasks, you would process this in the Python block definition.
            {% endcomment %}

            <div class="processed-content">
                {{ html_content }}
            </div>
        {% endif %}
    {% endwith %}
</div>




Alternative: Advanced processing in a custom StructValue class
For more robust processing, define a StructValue class to handle the BeautifulSoup logic. This approach keeps the template clean and separates business logic from presentation.
home/blocks.py (modified)

from wagtail import blocks
from bs4 import BeautifulSoup


class ProcessedHtmlStructValue(blocks.StructValue):
    def get_processed_html(self):
        # Access the raw_html field from the block's value
        raw_html = self.get('raw_html')

        # Check if there is any content to process
        if raw_html:
            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(raw_html, 'html.parser')

            # Example: Find all <h3> tags and add a custom CSS class
            for h3_tag in soup.find_all('h3'):
                h3_tag['class'] = h3_tag.get('class', []) + ['custom-h3-style']

            # Return the modified HTML as a string
            return str(soup)
        return ''


class HtmlProcessingBlock(blocks.StructBlock):
    raw_html = blocks.RichTextBlock(
        features=['h2', 'h3', 'bold', 'italic', 'link'],
        help_text='Enter the HTML content to be processed.'
    )

    class Meta:
        value_class = ProcessedHtmlStructValue
        template = 'home/blocks/html_processing_block.html'
        icon = 'code'
        label = 'HTML Processor'


# template/blocks/html_processing_block.html (modified)

{% load wagtailcore_tags %}
<div class="html-processor-block">
    {% comment %} Call the custom method on the block's value object {% endcomment %}
    <div class="processed-content">
        {{ value.get_processed_html|safe }}
    </div>
</div>

Step 4: Add the block to a StreamField
Now, you can include your new HtmlProcessingBlock in a StreamField on any of your Wagtail pages.
home/models.py

# models.py
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from .blocks import HtmlProcessingBlock

class HomePage(Page):
    body = StreamField([
        ('html_processor', HtmlProcessingBlock()),
        # ... other blocks
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

Step 5: Run database migrations
Since you have added a new block type to your StreamField, you need to run Django migrations.

python manage.py makemigrations
python manage.py migrate
