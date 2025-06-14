from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import Purchase


class PurchaseAdmin(ModelAdmin):
    model = Purchase
    base_url_path = "purchase-admin"  # customise the URL from default to admin/bookadmin
    menu_label = "Purchases"  # ditch this to use verbose_name_plural from model
    menu_icon = "link"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ("product_name", "user", "product_id", "purchase_id", "is_owner", "complete", "stripe_price", "timestamp")
    list_filter = ("user",)
    search_fields = ("product_name", "user")

modeladmin_register(PurchaseAdmin)
