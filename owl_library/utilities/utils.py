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
    transaction = Transaction.objects.filter(is_active=True,
                                                books__id=book_id
                                                ).first()
    if not transaction:
        return timezone.now()
    next_available_date = transaction.due_date + timedelta(days=1)
    user = CustomUser.objects.filter(email=email).first()
    if user:
        last_transaction = Transaction.objects.filter(user=user,
                                                        book=book_id
                                                        ).last()
        if last_transaction:
            # TODO Case where name starts with J
            lock_period = max([book.author.lock_period, book.lock_period])
            next_available_date = transaction.start_date + \
                                    timedelta(days=lock_period)
    return next_available_date