import pytest
from model_bakery import baker
from django.utils import timezone
from datetime import datetime, timedelta
from utilities.utils import (transaction_status_is_valid,
                                get_next_available_date,
                                get_date_after_lock_period,
                                calculate_next_date)
from users.models import CustomUser, Transaction
from books.models import Book



@pytest.mark.django_db
class TestDateCalculationHelpers(object):

    def test_calculate_next_date(self):
        '''
        Input: datetime object
        Ouput: datetime object
        If a past date is given as input, current 
        date is returned.
        If a future date is given as input, future
        date is returned.
        '''
        test_function = calculate_next_date
        past_date = timezone.now() - datetime(days=10)
        future_date = timezone.now() + datetime(days=10)
        assert test_function(future_date) == future_date
        assert test_function(past_date) == timezone.now().date()

    def test_calculate_next_date(self):
        author_1 = baker.make('Author',
                               name="Jack Ripper")
        book_1 = baker.make('Book',
                             title="book_1",
                             author=author_1,
                             )
        author_2 = baker.make('Author',
                               name="Uzumaki N")
        book_2 = baker.make('Book',
                             title="book_2",
                             author=author_2,
                             )
        test_function = get_date_after_lock_period
        now = timezone.now()
        assert test_function(now, book_1).date() ==\
                             (now + timedelta(days=180)).date()
        assert test_function(now, book_2).date() ==\
                             (now + timedelta(days=90)).date()


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
            Past inactive transaction held by email within
            lock period.
        7) Only Inactive/previous transaction(s)- held by email and 
            book's author name begin with 'J/j'.
        8) Only Inactive/previous transaction(s)- held by email, 
            book's author name does not begin with 'J/j'.
        9) Only Inactive transaction ,held by another user.
        10) Valid email. No history of transactions for the book.
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
        user_4 = baker.make('CustomUser',
                             username="user_4",
                             email="Stacy_Hamilton3144@jh02o.name")
        user_5 = baker.make('CustomUser',
                             username="user_5",
                             email="Harry_Hamilton3144@jh02o.name")
        author_1 = baker.make('Author',
                               name="Jack Ripper")
        author_2 = baker.make('Author',
                               name="Pack Ripper")
        author_3 = baker.make('Author',
                               name="Karl Marx")
        book_1 = baker.make('Book',
                             title="book_1",
                             author=author_1,
                             lock_period=180,
                             )

        book_2 = baker.make('Book',
                             title="book_2",
                             author=author_2,
                             lock_period=90)
        book_3 = baker.make('Book',
                             title="book_3",
                             author=author_1,
                             lock_period=90)
        book_4 = baker.make('Book',
                             title="book_4",
                             author=author_2,
                             lock_period=90)
        book_5 = baker.make('Book',
                             title="book_4",
                             author=author_2,
                             lock_period=90)
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
        transaction_3 = baker.make('Transaction',
                                     user=user_3,
                                     is_active=False,
                                     start_date=timezone.now() -\
                                      timedelta(days=60))
        transaction_3.books.add(book_1)
        transaction_4 = baker.make('Transaction',
                                    user=user_4,
                                    is_active=False,
                                    start_date=(timezone.now() -\
                                     timedelta(days=60)))
        transaction_4.books.add(book_3)
        transaction_5 = baker.make('Transaction',
                                    user=user_5,
                                    is_active=False,
                                    start_date=(timezone.now() -\
                                     timedelta(days=30)))
        transaction_5.books.add(book_4)
        # 1
        assert None == get_next_available_date(111)
        # 2
        assert timezone.now().date() == get_next_available_date(book_1.id).date()
        # 3
        assert None == get_next_available_date(book_1.id, "Dashales309@1wa8o.media")
        # 4
        assert (transaction_1.start_date + timedelta(days=180)).date() == get_next_available_date(book_1.id, "Enoch_Gilmore2863@evyvh.solutions").date()
        # 5
        assert (transaction_2.start_date + timedelta(days=90)).date() == get_next_available_date(book_2.id, "Dasha_Gonzales309@1wa8o.media").date()
        # 6
        assert (transaction_3.start_date + timedelta(days=180)).date() == get_next_available_date(book_1.id, "Phoebe_Hamilton3144@jh02o.name").date()
        # 7
        assert (transaction_4.start_date + timedelta(days=180)).date() == get_next_available_date(book_3.id, "Stacy_Hamilton3144@jh02o.name").date()
        # 8
        assert (transaction_5.start_date + timedelta(days=90)).date() == get_next_available_date(book_4.id, "Harry_Hamilton3144@jh02o.name").date()
        # 9
        assert timezone.now().date() == get_next_available_date(book_3.id, "Harry_Hamilton3144@jh02o.name").date()
        # 10
        assert timezone.now().date() == get_next_available_date(book_5.id, "Enoch_Gilmore2863@evyvh.solutions").date()



