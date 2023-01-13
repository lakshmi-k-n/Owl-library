from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book
from utilities.models import TimestampedModel
from django.conf import settings
# from datetime import datetime
from django.utils import timezone
# Create your models here.


class CustomUser(AbstractUser):
    address = models.CharField(null=True,
                            blank=True,
                            max_length=200)


class Transaction(TimestampedModel):
    # TRANSACTION_TYPES = (("BORROW", "Borrow"), ("RENEW", "Renew"))
    STATUSES = (("BORROWED", "Borrowed"), ("RENEWED", "Renewed"),
                            ("RETURNED", "Returned"), ("ABSCONDED", "Absconded"),
        )
    holding_period = 14

    notes = models.CharField(null=True,
                            blank=True,
                            max_length=200)
    transaction_status = models.CharField(max_length=10,
                                choices=STATUSES,
                                default="BORROWED")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="transactions",
                             on_delete=models.CASCADE)
    books = models.ManyToManyField(Book,
                                   related_name="transactions")
    start_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)