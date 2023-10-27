from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=255,unique=True)
    email = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []






class Book(models.Model):
    title = models.CharField(null=False, blank=False,max_length=255)
    author = models.CharField(null=False,blank=False,max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity_in_stock = models.PositiveIntegerField()
    publication_date = models.DateField(null=False)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title





class BookHistory(models.Model):
    related_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    edit_info = models.TextField(blank=True, null=True)
    edited_at = models.DateTimeField(auto_now_add=True,null=False)

    def __str__(self):
        return self


class BookReview(models.Model):
    related_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    related_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=False)

    def __str__(self):
        return self








