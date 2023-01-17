# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from utilities.models import TimestampedModel
from django.conf import settings

class Author(TimestampedModel):
    AUTHOR_TYPES = (("NOVELIST", "Novelist"), 
                    ("POET", "Poet"),
                    ("JOURNALIST", "Journalist"))
    name = models.CharField(max_length=150)
    bio = models.CharField(null=True,
                            blank=True,
                            max_length=200)
    author_type = models.CharField(max_length=20,
                                choices=AUTHOR_TYPES,
                                default="NOVELIST")
    # lock period in days
    lock_period = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Logic for saving lock period
         if self.name.startswith(('j','J')):
             self.lock_period = 180
         super().save(*args, **kwargs)


class Book(TimestampedModel):
    BOOK_TYPES = (("PAPERBACK", "Paperback"), 
                    ("HANDMADE", "Handmade"),
                    ("HARDCOVER", "Hardcover"))
    title = models.CharField(max_length=150)
    book_type = models.CharField(max_length=20,
                                choices=BOOK_TYPES,
                                default="PAPERBACK")
    publisher = models.CharField(max_length=150)
    author = models.ForeignKey(Author,
                             related_name="books",
                             on_delete=models.CASCADE)
    no_of_copies = models.IntegerField(default=0)
    description = models.CharField(null=True,
                            blank=True,
                            max_length=200)
    # lock period in days
    lock_period = models.IntegerField(default=90)
    is_active = models.BooleanField(default=True)