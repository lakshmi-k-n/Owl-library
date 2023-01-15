from rest_framework import serializers
from books.models import Book,Author
from users.models import CustomUser,Transaction
from utilities.utils import get_next_available_date


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book
    """
    class Meta:
        model = Book
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction
    """
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ('start_date', 'due_date', 'return_date',
                                'is_active')
