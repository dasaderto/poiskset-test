from django.urls import path
from rest_framework.routers import DefaultRouter

from books.app.handlers.books_handler import BooksHandler, BooksFilterHandler

urlpatterns = [
    path("filters/books/", BooksFilterHandler.as_view()),
]

router = DefaultRouter()
router.register("books", BooksHandler, basename='books')
urlpatterns += router.urls
