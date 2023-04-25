from django.db import models
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.db.models import Avg
import secrets
from .paystack import Paystack

# Create your models here.
class Category(models.Model):

    choice = models.CharField(max_length = 15)
    image = models.ImageField(upload_to='category/')
    slug = models.SlugField(max_length=200, unique=True)
    def __str__(self):
        return str(self.choice)
    def get_absolut_url(self):
        return reverse('Myapp:category_filter', args={self.slug})
class Product(models.Model):
    
    name = models.CharField(max_length=25) 
    image = models.ImageField(upload_to='products/') 
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.FloatField()
    choice = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name)
    
    def get_absolut_url(self):
        return reverse('Myapp:product_detail', args={self.slug, })
    
class Rating(models.Model):
    rating = models.IntegerField(default=0)
     
    def __str__(self):
        return str(self.rating)

class Feedback(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE )
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    feedback  = models.TextField(max_length=500)
    date = models.DateField(auto_now=True)
    rating = models.PositiveSmallIntegerField(choices=(
        (1, "⭐☆☆☆☆"),
        (2, "⭐⭐☆☆☆"),
        (3, "⭐⭐⭐☆☆"),
        (4, "⭐⭐⭐⭐☆"),
        (5, "⭐⭐⭐⭐⭐"),
    ))

   



class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField (max_length=50)
    image = models.ImageField(upload_to='proof/')
    phone = models.CharField (max_length=50)
    date = models.DateTimeField (auto_now=True)
    
    status = models.BooleanField (default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
    
    def __str__(self):
        return str(self.product.name)
    

class Orders(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField (max_length=50)
    image = models.ImageField(upload_to='proof/' ,null = True, blank= True )
    phone = models.CharField (max_length=50)
    date = models.DateTimeField (auto_now=True)
    
    status = models.BooleanField (default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
    
    def __str__(self):
        return str(self.product.name)
    
    def img_preview(self): 
        return mark_safe('<img src="/directory/%s" width="150" height="150" />' % {self.image.url})

    img_preview.short_description = 'Image'



class Payment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE,)
    amount = models.FloatField()
    ref = models.CharField(max_length=200)
    address = models.CharField (max_length=50)
   
    phone = models.CharField (max_length=50)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)
    def amount_value(self):
        return int(self.amount) * 100
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False