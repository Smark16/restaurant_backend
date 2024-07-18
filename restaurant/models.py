from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email= models.EmailField(max_length=100)
    verified = models.BooleanField(default=False)
    contact = models.PositiveIntegerField(default=000000000)
    image = models.ImageField(default='images/profile.jpg', upload_to='images/')
    location = models.CharField(max_length=100, default=None, null=True)
   

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email, verified=True)

def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)

class Menu(models.Model):
    descriptions = models.TextField()
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    image = models.ImageField(default='menu.jpg', upload_to='menu_images/')
    quantity = models.PositiveIntegerField(default=0)

    @property
    def avg_rating(self):
        ratings = self.ratings.all()
        print(ratings)
        if ratings:
            total_rates = sum([rating.value for rating in ratings])
            rating = total_rates / len(ratings)
            return rating
        else:
            return 0
        
    def get_avg_rating(self):
        my_item = self
        rating = my_item.avg_rating
        print(rating)
  

    def __str__(self):
        return f"{self.id}"

#total orders
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now=True)
    contact = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=100, null=True)
    #status_choices = (('Received', 'Received'), ('Pending', 'Pending'), ('Canceled', 'Canceled'),)
    status = models.CharField(max_length=100, default = "In Progress")

  
    def __str__(self):
        return f"{self.id}"
    
class OrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ManyToManyField(Menu, related_name='products')
    @property
    def total_quantity(self):
        total_quantity = 0
        for menu_item in self.menu.all():
            total_quantity += menu_item.quantity
        return total_quantity
    

def __str__(self):
    menu_names = [menu_item.name for menu_item in self.menu.all()]
    return ', '.join(menu_names) if menu_names else 'No Menu Items'

class Table(models.Model):
    table_no = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.table_no}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    contact = models.PositiveIntegerField(default=0)
    email = models.EmailField()
    party_size = models.PositiveIntegerField(default=0)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations', default=0)
    reservation_date = models.DateField()
    status = models.CharField(max_length=100, default = "Pending")

 
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    image = models.ImageField(default='images/profile.jpg', upload_to='images/')
    product = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='reviews_products', default=0)

class Rating(models.Model):
    product = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveIntegerField()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    message_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ('message_date', )
