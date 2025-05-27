from django.contrib import admin
from django.utils.html import format_html
from shop.models import Product, Category, ProductImage, Customer

# Register your models here.

admin.site.register(Category)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'image_preview']

    def product_name(self, obj):
        return obj.product.name

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 70px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'


class ImageTabularInline(admin.TabularInline):
    model = ProductImage
    extra = 2

    readonly_fields = ['image_preview']
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 70px;"/>', obj.image.url)

    image_preview.short_description = 'Image'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageTabularInline]
    list_display = ['id', 'name', 'price', 'quantity', 'category', 'image_preview']

    def image_preview(self, obj):
        first_image = obj.images.first()
        if first_image and first_image.image:
            return format_html('<img src="{}" style="height: 50px;"/>', first_image.image.url)
        return "-"
    image_preview.short_description = 'Image'


@admin.register(Customer)
class CostumerAdmin(admin.ModelAdmin):
    list_display = ['id','name']

