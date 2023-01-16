from users.models import CustomUser, Transaction
from books.models import Book
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist



def transaction_status_is_valid(status):
    from users.models import Transaction
    statuses = [tup[0] for tup in Transaction.STATUSES]
    return status.upper() in statuses

def get_next_available_date(book_id, email=None):
    # At a time,there will only be one active transaction for a book
    # since only one copy of each books exist. For now.
    try:
        book = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return None
    next_available_date = timezone.now()
    transactions = Transaction.objects.filter(books=book_id)
    # An inactive transaction would mean a book is returned
    # This is the case where a book is in borrowed state
    if transactions.filter(is_active=True):
        next_available_date = transactions.last().due_date + timedelta(days=1)
    #If email is provided, then we check lock conditions as well
    if email:
        last_transaction = transactions.filter(user__email=email,
                                                    ).last()
        # TODO Case where name starts with J
        lock_period = max([book.author.lock_period, book.lock_period])
        next_available_date = last_transaction.start_date + \
                                timedelta(days=lock_period)
    return next_available_date