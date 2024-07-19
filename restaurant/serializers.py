from rest_framework.fields import empty
from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','is_staff', 'is_customer', 'date_joined', 'email']

class obtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        token['is_customer'] = user.is_customer
        token['username'] = user.username
        token['email'] = user.email 
        token['image'] = str(user.profile.image)
        token['verified'] = user.profile.verified
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

    def to_representation(self, instance):
         response =  super().to_representation(instance)
         response['user'] = UserSerializer(instance.user).data
         return response


class OrderItemSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = OrderItems
        fields = ['id', 'user','order', 'menu', 'total_quantity']
        #depth = 1

    def to_representation(self, instance):
         response =  super().to_representation(instance)
         response['user'] = UserSerializer(instance.user).data
         response['order'] = OrderSerializer(instance.order).data
         response['menu'] = MenuSerializer(instance.menu.all(), many=True).data
         return response

class TableSerializer(serializers.ModelSerializer):
     class Meta:
          model = Table
          fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
     # user = serializers.ReadOnlyField(source='user.username')
     class Meta:
          model = Reservation
          fields =  ['id','user','contact', 'email', 'party_size','table', 'reservation_date', 'status']

     def to_representation(self, instance):
         response =  super().to_representation(instance)
         response['user'] = UserSerializer(instance.user).data
         return response


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
          fields = ['id', 'user', 'email','contact', 'image', 'location']

# change password
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        # Check if the new password and its confirmation match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        # Verify that the provided old password matches the user's current password
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        # make sure user is only able to update their own password
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You don't have permission for this user."})

        # Set the new password for the user instance
        instance.set_password(validated_data['password'])
        instance.save()

        return instance