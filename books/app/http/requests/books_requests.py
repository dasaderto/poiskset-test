import itertools

from rest_framework import serializers

from books.models import Book
from core.utils.serializers import UnimplementedSerializer


class BooksFilterRequest(UnimplementedSerializer):
    user_id = serializers.IntegerField()
    name = serializers.CharField()
    sorting = serializers.ListField(child=serializers.ChoiceField(
        choices=list(itertools.chain(*[[field_name, f"-{field_name}"] for field_name in [
            Book.genre.field.name,
            Book.pages_count.field.name,
            Book.author.field.name,
            Book.has_cover.field.name,
        ]]))
    ))
