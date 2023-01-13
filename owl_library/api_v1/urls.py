from django.conf.urls import url
from rest_framework import routers
from .views import (BooksViewSet, 
                    TransactionsViewSet,
                    CheckBookAvailabilityAPI)
from rest_framework_swagger.views import get_swagger_view


urlpatterns = []

router = routers.SimpleRouter()
router.register(r'books',
                BooksViewSet, 'books')
router.register(r'users/(?P<user_id>.+)/transactions',
                TransactionsViewSet, 'user_transactions')
urlpatterns += url("^books/next-available/$",
                   view=CheckBookAvailabilityAPI.as_view(),
                    name="next-available"),
# router.register(r'users/transactions',
#                 TransactionsViewSet, 'user_transactions')
urlpatterns += router.urls