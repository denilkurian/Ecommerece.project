from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.views.generic import FormView

Type1 =(
    ("Science", "Science"),
    ("Commercial", "Commercial"),
    ("Historical", "Historical"),
  ("Fantasy", "Fantasy"),
    ("Drama", "Drama"),
    ("History", "History"),
("Adventure", "Adventure"),
    ("Cartoon", "Cartoon"),
    ("Fairytale", "Fairytale"),
    ("Alphabets", "Alphabets"),
)

class Book(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE ,blank=True, null=True)
    book_type = models.CharField(max_length=200, choices=Type1)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    image_url = models.CharField(max_length=2000, blank=True)
    genre=models.CharField(max_length=200)
    book_available = models.BooleanField(blank=True)

    def __str__(self):
        return self.title



#
# class Order(models.Model):
#     product = models.ForeignKey(Book,max_length=200,null=True,blank=True,on_delete=models.SET_NULL)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.product.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    image_url = models.CharField(max_length = 2083, default=False)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)




class Review(models.Model):
    product = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()






