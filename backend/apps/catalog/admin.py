from django.contrib import admin
from .models import Product, Tag, ProductImage, Review
from apps.categories.models import CategoryImage, Category, Subcategory, SubcategoryImage


class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 1
    fields = ('src', 'alt', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.src:
            return f'<img src="{obj.src.url}" style="max-height: 100px; max-width: 100px;" />'
        return "Нет изображения"
    image_preview.short_description = 'Превью'
    image_preview.allow_tags = True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title',)
    inlines = [CategoryImageInline]

class SubcategoryImageInline(admin.TabularInline):
    model = SubcategoryImage
    extra = 1
    fields = ('src', 'alt', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.src:
            return f'<img src="{obj.src.url}" style="max-height: 100px; max-width: 100px;" />'
        return "Нет изображения"
    image_preview.short_description = 'Превью'
    image_preview.allow_tags = True


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)
    inlines = [SubcategoryImageInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rate',)
    list_display_links = ('rate',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('src', 'alt', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.src:
            return f'<img src="{obj.src.url}" style="max-height: 100px; max-width: 100px;" />'
        return "Нет изображения"
    image_preview.short_description = 'Превью'
    image_preview.allow_tags = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'freeDelivery',)
    list_display_links = ('title',)
    list_filter = ('freeDelivery',)
    list_editable = ('price', 'stock', 'freeDelivery',)
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'alt')
    list_filter = ('product',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.src:
            return f'<img src="{obj.src.url}" style="max-height: 100px; max-width: 100px;" />'
        return "Нет изображения"
    image_preview.short_description = 'Превью'
