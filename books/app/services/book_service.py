from dataclasses import dataclass
from typing import List, Optional

from django.db.models import Q

from books.models import Book


@dataclass
class BooksFilterData:
    user_id: Optional[int] = None
    name: Optional[str] = None
    sorting: Optional[List[str]] = None


class BooksFilter:
    def __init__(self, data: BooksFilterData):
        self.data = data

    def filter(self):
        books_filter_query = Q()

        if self.data.user_id:
            books_filter_query &= Q(user_id=self.data.user_id)

        if self.data.name:
            books_filter_query &= Q(name=self.data.name)

        return Book.objects.filter(books_filter_query)
