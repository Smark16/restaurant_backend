from django.urls import path
from . import views


urlpatterns = [
    #user urls
    path('', views.ObtainPairView.as_view()),
    path('users', views.list_Users.as_view()),
    path('single_user/<int:pk>', views.single_user.as_view()),
    path('register', views.RegisterView.as_view()),
    path('dashboard', views.dashboard),
    path('profiles', views.all_profiles.as_view()),
    path('update_profile/<int:pk>', views.update_profile.as_view()),
    path('profile/<int:pk>', views.user_profile.as_view()),

    #menu urls
    path('food_items', views.list_menu.as_view()),
    path('food_items/<int:pk>', views.single_item.as_view()),
    path('rating', views.ratings.as_view()),
    path('orders', views.OrderList.as_view()),
    path('orders/<int:pk>', views.singleOrder.as_view()),
    path('order_detail/<int:pk>', views.orderDetail.as_view()),
    path('latest_orders', views.LatestOrder.as_view()),
    path('userOrder/<int:user>', views.getUserOrder),

    #reservation urls
    path('reservation', views.reservation.as_view()),
    path('reservation/<int:id>', views.single_reservation),
    path("update_reservation/<int:pk>", views.UpdateReservationStatus.as_view()),
    path("user-reservation/<int:user>", views.UserReservations),

    path('reviews', views.reviews.as_view()),
    path('message',views.message.as_view()),

    #posturls
    path('items', views.ItemsViewSet.as_view()),
    path('single_item/<int:pk>', views.single_order.as_view()),
    path('update_order/<int:pk>', views.update_order.as_view()),
    path('delete_order/<int:pk>', views.DeleteOrder.as_view()),
    path('update_status/<int:pk>', views.UpdateOrderStatus.as_view()),
    path('placed_orders', views.PlacedOrder.as_view()),
    path('order_items', views.OrderItem.as_view()),
    path('post_OrderItems', views.PostOrderItems.as_view()),

    #user_urls
    path('update-username', views.UpdateUsername.as_view(), name='update-username'),
    path('forgot_password', views.forgot_password),
    path('tables', views.Tables.as_view()),
    path('new_reservation', views.newReservations.as_view()),

    #ratings
    path('rates', views.Rates.as_view()),
    path('ratings', views.Ratings.as_view()),
    path('rating/<int:pk>', views.singleRating.as_view()),

    #reviews
    path('reviews', views.listReviews.as_view()),
    path('post_review', views.newReview.as_view()),
    path('product_review/<int:menu_id>', views.productReview.as_view()),

    #Notificaions
    path('messages', views.Messages.as_view()),
]