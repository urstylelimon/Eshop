from django.db import models

class Category (models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100)
    image = models.ImageField(upload_to = 'images/', blank = True, null = True)

    def __str__(self):
        return self.name

class Product (models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    #1. This is the main Image
    image = models.ImageField(upload_to = 'products/')

    # 2. Add these three new optional image fields
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)