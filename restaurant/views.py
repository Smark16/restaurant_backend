from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework.permissions import BasePermission

class CanUpdateUsername(BasePermission):
    def has_permission(self, request, view):
        # Check if the user can update their username
        return request.user.is_authenticated and request.user.has_perm('change_user_username')

# Create your views here.
class ObtainPairView(TokenObtainPairView):
    serializer_class = obtainSerializer

class list_Users(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class single_user(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == 'GET':
        response = f"Hey {request.user} you sent a get request"
        return Response({'response':response}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        text = request.POST.get('text')
        response = f"Hey {request.user}, ur text is {text}"
        return Response({'response':response}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)

class list_menu(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class single_item(generics.RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Menu.DoesNotExist:
            return Response({'detail':'item does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
        
class ratings(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class singleOrder(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OrderList.DoesNotExist:
            return Response({'detail': 'Order Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

class LatestOrder(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        current_date = date.today()
        queryset = Order.objects.filter(order_date=current_date)
        return queryset
class reservation(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

@api_view(['GET'])
def UserReservations(request, user):
    try:
        UserReservation = Reservation.objects.filter(user=user)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serialize = ReservationSerializer(UserReservation, many=True)
        return Response(serialize.data)

#correct code
@api_view(['GET'])
def getUserOrder(request, user):
    try:
        userOrder = Order.objects.filter(user=user)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serialize = OrderSerializer(userOrder, many=True)
        return Response(serialize.data)

def single_reservation(request, id):
    try:
        booking = Reservation.objects.get(pk=id)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serialize = ReservationSerializer(booking)
        return Response(serialize.data)

class reviews(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class message(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class all_profiles(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class user_profile(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"detail":"Profile not Found"}, status=status.HTTP_404_NOT_FOUND)
        
#post menu_items
class ItemsViewSet(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
       serializers = MenuSerializer(data=request.data)
       if serializers.is_valid():
           serializers.save()
           return Response(serializers.data, status=status.HTTP_201_CREATED)
       else:
           return Response(serializers.errors, status=status.HTTP_403_FORBIDDEN)
       
#delete menu_item
class single_order(generics.RetrieveDestroyAPIView):  
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    permission_classes = [AllowAny]  

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrderItem(generics.ListCreateAPIView):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemSerializer

   
#order-Deatil
class orderDetail(generics.ListAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id = order_id)
        order_item = OrderItems.objects.filter(order=order)
        return order_item

#delete placed_order    
class DeletePlacedOrder(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response("Deleted Successfully", status=status.HTTP_301_MOVED_PERMANENTLY)
    
#update menu_item
class update_order(generics.UpdateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UpdateOrderStatus(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def patch(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        new_status = request.data.get("newStatus")

        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save()

            serializer = self.serializer_class(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

#place an order     
class PlacedOrder(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
         serializers = OrderSerializer(data=request.data)
         if serializers.is_valid():
           serializers.save()
           return Response(serializers.data, status=status.HTTP_201_CREATED)
         else:
           return Response(serializers.errors, status=status.HTTP_403_FORBIDDEN)


     
class UpdateReservationStatus(APIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def patch(self, request, *args, **kwargs):
        reserve_id = kwargs.get('pk')
        new_status = request.data.get("newStatus")

        try:
            reservation = Reservation.objects.get(pk=reserve_id)
            reservation.status = new_status
            reservation.save()

            serializer = self.serializer_class(reservation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except reservation.DoesNotExist:
            return Response({"error": "Reservation doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    
#update profile
class update_profile(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class =  ProfileSerializer

    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeleteOrder(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#display Tables
class Tables(generics.ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    
class newReservations(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def create(self, request, *args, **kwargs):
        response = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response['data'] = serializer.data
        response['response'] = "Table is successfully booked"
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


    def post(self, request, *args, **kwargs):
        table = get_object_or_404(Table, pk=request.data['table'])
        if table.is_booked:
            return Response({"response": "Table is already booked"}, status=status.HTTP_200_OK)
        table.is_booked = True
        table.save()
        return self.create(request, *args, **kwargs)

#update username
class UpdateUsername(APIView):
    permission_classes = [IsAuthenticated, CanUpdateUsername]

    def put(self, request, *args, **kwargs):
        new_username = request.data.get('new_username', None)

        if new_username:
            user = request.user
            user.username = new_username
            user.save()

            new_serializer = UserSerializer(user)
            # Ensure the user stays logged in after username change
            update_session_auth_hash(request, user)

            return Response({'message': 'Username updated successfully.'},new_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'New username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
class Ratings(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class Rates(APIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def post(self, request, format=None):
        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        
class singleRating(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ratings.DoesNotExist:
            return Response({'detail': 'Order Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

class listReviews(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class newReview(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class productReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Get the menu item id from the URL parameter
        menu_id = self.kwargs['menu_id']
        
        # Fetch the menu object or return 404 if not found
        menu = get_object_or_404(Menu, id=menu_id)

        # Filter reviews based on the menu item
        queryset = Review.objects.filter(product=menu)
        return queryset
    
class Messages(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    
#reset_password
@csrf_exempt
def forgot_password(request):
    email = request.POST.get("email")
    print(f"Received email: {email}")
    verify = User.objects.filter(email=email).first()
    if verify:
        link = f"http://localhost:5173/forgot-password/{verify.id}"
        send_mail(
            'verify Account',
            'please verify Your Account',
            'smark@gmail.com',
            [email],
            fail_silently=False,
            html_message=f"<p>Click on the LINK below</p><p>{link}</p>"
        )
        # Instead of returning a raw dictionary, return a JsonResponse
        return JsonResponse({"bool":True, "user_id":verify.id}, status=status.HTTP_200_OK)
    else:
        # Similarly, return a JsonResponse here as well
        return JsonResponse({"bool":False}, status=status.HTTP_403_FORBIDDEN)