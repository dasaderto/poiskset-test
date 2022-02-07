from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from books.app.http.requests.books_requests import BooksFilterRequest
from books.app.http.resources.books_resources import BookResource
from books.app.services.book_service import BooksFilterData, BooksFilter
from books.models import Book
from core.utils.pagination import paginate


class BooksHandler(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class = BookResource
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {
            'ctx_user': self.request.user
        }

    def get_queryset(self):
        return Book.objects.filter(user_id=self.request.user.id)


class BooksFilterHandler(GenericAPIView):
    serializer_class = BooksFilterRequest

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=self.request.data, partial=True)
        data.is_valid(raise_exception=True)
        filter_data = BooksFilterData(**data.validated_data)
        filtered_books = BooksFilter(data=filter_data).filter()

        return Response(paginate(data=filtered_books,
                                 page=self.request.GET.get('page', 1),
                                 per_page=self.request.GET.get('per_page', 15),
                                 resource=BookResource,
                                 sorting=filter_data.sorting))
