import pytest
from model_bakery import baker
from django.utils import timezone
from datetime import datetime, timedelta
from utilities.utils import (transaction_status_is_valid,
                                get_next_available_date)
from users.models import CustomUser, Transaction
from books.models import Book


@pytest.mark.django_db
class TestTransactionStatus(object):

    @pytest.mark.parametrize("test_input,expected", [
        ("stop", False),
        ("BORROWED", True),
        ("RETURNED", True),
        ("ABSCONDED", True),
        ("RENEWED", True),
        ("renewed", True),
        ("returned", True),
        ("HASJHK", False)
    ])
    def test_transaction_status_is_valid(self, test_input, expected):
        test_function = transaction_status_is_valid
        assert test_function(test_input) == expected



@pytest.mark.django_db
class TestNextAvailableDate(object):

    def test_get_next_available_date(self):
        ''' 
        Testing function : get_next_available_date

        Test cases: 
        1) Invalid book id
        2) Valid book id but email not provided
        3) Valid book id, no user record for email
        4) Active transaction held by email and book's
            author name starts with 'J/j'.
        5) Active transaction held by email and book's
            author name does not start with 'J/j'.
        6) Active transaction held by another user.
        7) Inactive/previous transaction(s) held by email and 
            book's author name begin with 'J/j'.
        8) Inactive/previous transaction(s) held by email and 
            book's author name does not begin with 'J/j'.
        9) Active transaction held by another user.
        10) No history of transactions for the book.
        '''
        user_1 = baker.make('CustomUser',
                             username="user_1",
                             email="Enoch_Gilmore2863@evyvh.solutions")
        user_2 = baker.make('CustomUser',
                             username="user_2",
                             email="Dasha_Gonzales309@1wa8o.media")
        user_3 = baker.make('CustomUser',
                             username="user_3",
                             email="Phoebe_Hamilton3144@jh02o.name")
        author_1 = baker.make('Author',
                               name="Jack Ripper")
        author_2 = baker.make('Author',
                               name="Pack Ripper")
        book_1 = baker.make('Book',
                             title="book_1",
                             author=author_1,
                             lock_period=180,
                             )

        book_2 = baker.make('Book',
                             title="book_2",
                             author=author_2,
                             lock_period=60)
        transaction_1 = baker.make('Transaction',
                                    user=user_1,
                                    is_active=True,
                                    start_date=(timezone.now() -\
                                     timedelta(days=4)))

        transaction_1.books.add(book_1)
        transaction_2 = baker.make('Transaction',
                                     user=user_2,
                                     is_active=True,
                                     start_date=timezone.now() -\
                                      timedelta(days=10))
        transaction_2.books.add(book_2)
