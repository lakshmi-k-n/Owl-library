from rest_framework import serializers
from books.models import Book,Author
from users.models import CustomUser,Transaction


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book
    """
    class Meta:
        model = Book
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Book
    """
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ('start_date', 'due_date', 'return_date',
                                'is_active')
