from rest_framework import serializers
from books.models import Book,Author
from users.models import CustomUser,Transaction
from utilities.utils import get_next_available_date


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book
    """
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_author_name(self, obj):
        return obj.author.name



class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction
    """
    book = serializers.PrimaryKeyRelatedField(
                    queryset=Book.objects.all()
                    ,write_only=True)
    book_title = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('id','start_date', 'due_date', 'return_date',
                    'is_active','transaction_status','book','book_title',
                    'book_title','author_name'
                    )
        read_only_fields = ('id','start_date', 'due_date', 'return_date',
                            'book_title','is_active','transaction_status',
                            'author_name')

    def get_book_title(self, obj):
        book = obj.books.first()
        return book.title

    def get_author_name(self, obj):
        book = obj.books.first()
        return book.author.name
