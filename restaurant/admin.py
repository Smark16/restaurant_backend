from django.contrib import admin
from .models import *
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user', 'email','image', 'location','contact','verified']

class MenuAdmin(admin.ModelAdmin):
    list_display = ['id','descriptions','name', 'price', 'image', 'avg_rating']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'contact', 'location', 'status']

class OrderItemAdmin(admin.ModelAdmin):
    filter_horizontal = ("menu", )
    list_display = ['id','user', 'order', 'total_quantity', 'get_menus']

    def get_menus(self, obj):
        return ", ".join([menu.name for menu in obj.menu.all()])
    get_menus.short_description = 'Menus'  # Optional: to provide a header for the column


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user','contact', 'email', 'party_size','table', 'reservation_date','status']

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'review', 'image', 'product']

class RatingsAdmin(admin.ModelAdmin):
    list_display = ['product', 'value']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','message', 'message_date']

class TableAdmin(admin.ModelAdmin):
    list_display = ['id', 'table_no']

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username','email','is_staff', 'is_customer', 'date_joined']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(Rating, RatingsAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(OrderItems, OrderItemAdmin)
