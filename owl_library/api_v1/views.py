# from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from books.models import Book, Author
from users.models import CustomUser, Transaction
from .serializers import BookSerializer, TransactionSerializer
from utilities.utils import (transaction_status_is_valid,
                                get_next_available_date)
# from utilities.authentication import EmailAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.http.response import Http404
# Create your views here.


class BooksViewSet(mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    '''
    View to list books
    '''
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CamelCaseJSONRenderer,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = BookSerializer
    lookup_field = ('id')

    def get_queryset(self):
        author_id = self.request.query_params.get('author', None)
        author_name = self.request.query_params.get('authorName', None)
        books = Book.objects.all().order_by("-id")
        # if both id and name is obtained,id is used
        if author_id:
            books = books.filter(author=author_id)
        elif author_name:
            authors = Author.objects.filter(name__istartswith=author_name)
            books = books.filter(author__in=authors)
        return books


class CheckBookAvailabilityAPI(APIView):
    """
    """
    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email',None)
        # bookId is required
        book_id = request.query_params.get('bookId',None)
        if not book_id:
            raise Http404
        next_available = get_next_available_date(book_id, email=email)
        return Response({"next_available": next_available}, 
                                    status=status.HTTP_200_OK)


class TransactionsViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CamelCaseJSONRenderer,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = TransactionSerializer
    lookup_field = ('id')

    def create(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        # import pdb
        # pdb.set_trace()
        data = request.data
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message":"success"},
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, **kwargs):
        user_id = kwargs.get('user_id',None)
        transaction_id = kwargs.get('id',None)
        transaction_status = request.data.get('status',None)
        # user_email = request.data.get('user_id',None)
        # import pdb
        # pdb.set_trace()
        if not transaction_status_is_valid(transaction_status):
            return Response({"error": "invalid data"},
                             status=status.HTTP_400_BAD_REQUEST)
        if not user_id and not transaction_id:
            raise Http404
        try:
            transaction = Transaction.objects.get(id=transaction_id,
                                                    user=user_id)
        except ObjectDoesNotExist:
            raise Http404
        transaction.status = upper(transaction_status)
        transaction.return_date = timezone.now()
        transaction.is_active = False
        transaction.save()
        return Response(
            {"message":"success"},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def active(self, request, **kwargs):
        user_id = kwargs.get('user_id',None)
        if not user_id:
            raise Http404
        active_transactions = Transaction.objects.filter(user=user_id,
                                                    is_active=True
                                                    ).order_by('-id')

        serializer = self.serializer_class(active_transactions, many=True)
        return Response(serializer.data)
