from django.db import models
from django.contrib.auth.models import User


class books(models.Model):
    Book_name=models.CharField(max_length=50,default='')
    description=models.CharField(max_length=500,default='')
    pub_date=models.DateField()
    author=models.CharField(max_length=50,default="")
    category=models.CharField(max_length=50,default="")
    img=models.ImageField(upload_to='book_img',default='')
    def __str__(self):
        return self.Book_name
        return self.img
        return self.description
        return self.img
