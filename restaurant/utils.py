from pyfcm import FCMNotification
from django.conf import settings

def send_push_notification(fcm_token,notification_title, notification_body, notification_image=None):
    push_service = FCMNotification(project_id="restaurant-management-sy-4c2c8", service_account_file=settings.FCM_SERVICE_ACCOUNT_FILE)
    
    result = push_service.notify(
       fcm_token=fcm_token, 
       notification_title=notification_title, 
       notification_body=notification_body, 
       notification_image=notification_image
    )
    print(result)
    return result

