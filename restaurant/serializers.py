from rest_framework.fields import empty
from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','is_staff', 'is_customer']

class obtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        token['is_customer'] = user.is_customer
        token['username'] = user.username
        token['full_name'] = user.profile.full_name
        token['email'] = user.email 
        token['image'] = str(user.profile.image)
        token['verified'] = user.profile.verified
        token['gender'] = user.profile.gender
        token['location'] = user.profile.location
        token['contact'] = user.profile.contact

        return token

class RegisterSerializer(serializers.ModelSerializer):
        password = serializers.CharField(
             write_only=True, required = True, validators = [validate_password]
        )
        class Meta:
             model = User
             fields = ['id', 'email', 'username', 'password', 'is_staff', 'is_customer']

        def create(self, validated_data):
             user = User.objects.create(
                  username = validated_data['username'],
                  email = validated_data['email'],
                  is_staff = validated_data.get('is_staff', False),
                  is_customer = validated_data.get('is_customer', False)
             )
             user.set_password(validated_data['password'])
             user.save()
             return user
        
class RatingSerializer(serializers.ModelSerializer):
     class Meta:
          model = Rating
          fields = ['id', 'product', 'value']

class MenuSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
            max_length=None, use_url=True
        )

    class Meta:
        model = Menu
        fields = ['id','descriptions', 'name', 'price', 'image', 'quantity', 'avg_rating']
       



class OrderSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'contact', 'location', 'status']

    #def __init__(self, *args, **kwargs):
          #super(OrderSerializer, self).__init__(*args, **kwargs)
          #self.Meta.depth = 1


class OrderItemSerializer(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all(), many=True)

    class Meta:
        model = OrderItems
        fields = ['id', 'user','order', 'menu', 'total_quantity']
        #depth = 1

   # def __init__(self, *args, **kwargs):
          #super(OrderItemSerializer, self).__init__(*args, **kwargs)
          #self.Meta.depth = 1

class TableSerializer(serializers.ModelSerializer):
     class Meta:
          model = Table
          fields = ["id", "table_no"]

class ReservationSerializer(serializers.ModelSerializer):
     # user = serializers.ReadOnlyField(source='user.username')
     class Meta:
          model = Reservation
          fields =  ['id','user','contact', 'email', 'party_size','table', 'reservation_date', 'status']

class ReviewSerializer(serializers.ModelSerializer):
     #image = serializers.ReadOnlyField(source='profile.image')
     class Meta:
          model = Review
          fields = ['id','user','review', 'image', 'product']

class NotificationSerializer(serializers.ModelSerializer):
     user = serializers.ReadOnlyField(source='user.username')
     class Meta:
          model = Notification
          fields = ['id', 'message', 'message_date', 'user']

class ProfileSerializer(serializers.ModelSerializer):
     user = serializers.ReadOnlyField(source='user.username')
     class Meta:
          model = Profile
          fields = ['id', 'user', 'email', 'full_name', 'contact', 'image', 'location', 'gender' ]