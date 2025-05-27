from enum import unique

from django.db import models
from decimal import Decimal
from django.db.models import Avg
from django.db.models.functions import Round
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default = 1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null =True, blank = True, related_name='products')
    discount = models.DecimalField(max_digits=14, decimal_places=2, default = 0)
    def __str__(self):
        return self.name

    @property
    def first_image(self):
        if self.images:
            return self.images.first()

    @property
    def discounted_price(self):
        return self.price * Decimal(f'{1 - (self.discount/100)}')

    @property
    def avg_rating(self):
        avg = self.comments.aggregate(avg=Round(Avg('rating'), precision=2))['avg']
        return round(avg or 0)

class ProductImage(BaseModel):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null =True, blank = True, related_name='images')

    def __str__(self):
        return self.product.name

class Customer(BaseModel):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    billing_address = models.CharField(max_length=100, default='tashkent')
    phone = models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to='customers/', blank=True, null=True, default='customers/blank-profile-picture-973460_1280.webp')

    def __str__(self):
        return self.name

class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=30)
    email = models.EmailField()
    content = models.TextField()
    rating = models.IntegerField(choices=RatingChoices.choices)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null =True, blank = True, related_name='comments')

    def __str__(self):
        return self.name








