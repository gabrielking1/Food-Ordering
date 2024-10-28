from django.contrib import admin
from .models import Product,Category,Order,Rating,Feedback, Payment
from django.contrib import messages
from django.utils.translation import ngettext
from django.utils.html import format_html
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('choice', 'slug')
    prepopulated_fields = {'slug': ('choice',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    prepopulated_fields = {'slug': ('name',)}
# admin.site.register(Product, ProductAdmin)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def marked_seen(self, request, queryset):
        for obj in queryset:
            if obj.status == False:
                updated = queryset.update(status='True')
                self.message_user(request, ngettext(
                    '%d Transaction was successful',
                    '%d Transactions were successful.',
                    updated,
                ) % updated, messages.SUCCESS)
                
            
                
            else:
                self.message_user(request,
                    'Error transaction already Apporoved.',  messages.ERROR)
                
            
    def image_tag(self, obj):
        default_image_url = '/Myapp/succ.jpg'
        c = []
        if obj.image:
            return format_html('<img src="{}" width="150" height="150"/>'.format(obj.image.url))
        # obj.image.url
        else:

            return format_html('<img src="{}" width="150" height="150"/>'.format(default_image_url))

    image_tag.short_description = 'Image'
    
    
    
    list_display = ('product', 'status',
                    'image_tag',
                    )
    search_fields = ("customer__username__icontains", )
    
    actions = [marked_seen]



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('username', 'product','rating',)
    # prepopulated_fields = {'slug': ('choice',)}

class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating',)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('customer','product','price',)
#     search_fields = ("customer__username__icontains", )

admin.site.register(Rating, RatingAdmin)
admin.site.register(Payment)
# admin.site.register(Order, OrderAdmin)