from django.db import models
from django.contrib.auth.models import User

from django.db.models import Avg, Count

# Create your models here.

class ProductCategories(models.Model):
    CHOOSE = (
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Children', 'Children'),
        ('Unisex', 'Unisex'),
    )
    categorie_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20,choices=CHOOSE)
    def __str__(self):
        return self.categorie_name

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    image=models.ImageField(upload_to='images/',null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount=models.IntegerField(default=0)
    minamount=models.IntegerField(default=3)
    detail=models.TextField(max_length=500)
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    categorie=models.ForeignKey(ProductCategories,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    def avaregereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
        avg=0
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

class Comment(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length=250,blank=True)
    subject = models.CharField(max_length=100,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20,blank=True)
    status=models.CharField(max_length=10,choices=STATUS,default='True')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject