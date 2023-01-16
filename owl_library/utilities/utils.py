from users.models import CustomUser, Transaction
from books.models import Book
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist



def transaction_status_is_valid(status):
    from users.models import Transaction
    statuses = [tup[0] for tup in Transaction.STATUSES]
    return status.upper() in statuses

# def get_next_available_date(book_id, email=None):
#     # At a time,there will only be one active transaction for a book
#     # since only one copy of each books exist. For now.
#     try:
#         book = Book.objects.get(id=book_id)
#     except ObjectDoesNotExist:
#         return None
#     next_available_date = timezone.now()
#     transactions = Transaction.objects.filter(books=book_id)
#     # An inactive transaction would mean a book is returned
#     # This is the case where a book is in borrowed state
#     if transactions.filter(is_active=True):
#         next_available_date = transactions.last().due_date + timedelta(days=1)
#     #If email is provided, then we check lock conditions as well
#     if email:
#         last_transaction = transactions.filter(user__email=email,
#                                                     ).last()
#         if not last_transaction:
#             return None
#         # TODO Case where name starts with J
#         lock_period = max([book.author.lock_period, book.lock_period])
#         next_available_date = last_transaction.start_date + \
#                                 timedelta(days=lock_period)
#     return next_available_date
def get_date_after_lock_period(book):
    lock_period =  max(
            [book.author.lock_period,
                     book.lock_period])
    return timezone.now() + timedelta(days=lock_period)


def calculate_next_date(date_obj):
    if date_obj < timezone.now():
        return timezone.now()
    return date_obj


def get_next_available_date(book_id, email=None):
    '''
    Input: Takes book id, and email
    Output: None or date object
    '''
    try:
        book = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return None
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
    inactive_transactions = transactions.filter(is_active=False)
    # If there is an active transaction for the book
    if active_transaction:
        # current_transaction = active_transactions.last()
        if active_transaction.user == user:
            return get_date_after_lock_period(book)
        else:
            return calculate_next_date(
                        active_transaction.due_date
                                    )
    # If there are inactive/previous transactions for the book
    elif inactive_transactions:
        last_transaction = inactive_transactions.last()
        if last_transaction.user == user:
            return get_date_after_lock_period(book)
        else:
            return calculate_next_date(
                        last_transaction.due_date
                                    )
    #If there are no transaction history for the book
    else:
        return timezone.now()



