from users.models import CustomUser, Transaction
from books.models import Book
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


def transaction_status_is_valid(status):
    from users.models import Transaction
    statuses = [tup[0] for tup in Transaction.STATUSES]
    return status.upper() in statuses

def calculate_next_date(date_obj):
    if date_obj > timezone.now():
        return date_obj
    return timezone.now()

def get_date_after_lock_period(start_date, book):
    lock_period =  max(
            [book.author.lock_period,
                     book.lock_period])
    date = start_date + timedelta(days=lock_period)
    return calculate_next_date(date)

def get_next_available_date(book_id, email=None):
    '''
    Input: Takes book id, and email
    Output: None or date object
    '''
    try:
        book = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return None
    # If no email provided, return current date
    if not email:
        return timezone.now()
    try:
        user = CustomUser.objects.get(email=email)
    except ObjectDoesNotExist:
        return None
    # Valid email and book
    transactions = Transaction.objects.filter(books=book)
    # Current/active transaction for the book (only one 
    # active transaction can exist for a book at a time). 
    active_transaction = transactions.filter(
                                        is_active=True
                                        ).last()
    # Past/inactive transactions for the book
    inactive_transactions = transactions.filter(
                                        is_active=False
                                        )
    # If there is an active transaction for the book
    if active_transaction:
        if active_transaction.user == user:
            return get_date_after_lock_period(
                            active_transaction.start_date ,
                                                book)
        else:
            last_inactive_transaction = \
                        inactive_transactions.filter(
                            user=user).last()
            if last_inactive_transaction:
                return get_date_after_lock_period(
                            last_inactive_transaction.start_date ,
                                                book)
            else:
                return calculate_next_date(
                            active_transaction.due_date
                                        )
    # If there are inactive/previous transactions for the book
    elif inactive_transactions:
        last_transaction = inactive_transactions.last()
        if last_transaction.user == user:
            return get_date_after_lock_period(
                            last_transaction.start_date ,
                                                book)
        else:
            return timezone.now()
    #If there are no transaction history for the book
    else:
        return timezone.now()



