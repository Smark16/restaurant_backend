# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from django.contrib.auth import get_user_model
# from .models import Notification, Profile

# User = get_user_model()

# @receiver(post_save, sender=Notification)
# def notification_created(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'test',
#             {
#                 "type": "send_notification",
#                 "message": instance.message
#             }
#         )

# @receiver(post_save, sender=User)
# def user_registered_notification(sender, instance, created, **kwargs):
#     if created:
#         admin_user = User.objects.filter(is_superuser=True).first()  # Assuming first superuser is an admin
#         if admin_user:
#             Notification.objects.create(
#                 user=admin_user,
#                 message=f"New user registered: {instance.username}"
#             )
