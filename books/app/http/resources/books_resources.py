from rest_framework import serializers

from books.models import Book


class BookResource(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ['user']

    def create(self, validated_data):
        return Book.objects.create(**validated_data, user=self.context.get('ctx_user'))