from rest_framework import serializers

from books.models import BookModel


# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookModel
#         fields = '__all__'


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    content = serializers.CharField(max_length=255)
    isbn = serializers.CharField(max_length=13)
    subtitle = serializers.CharField(max_length=255)
    pages = serializers.IntegerField()
    in_stock = serializers.BooleanField(default=False)

    def validate(self, attrs):
        isbn = attrs.get('isbn')
        if BookModel.objects.filter(isbn=isbn).exists():
            raise serializers.ValidationError("This ISBN is already exists.")
        elif len(isbn) != 13:
            raise serializers.ValidationError("ISBN should be 13 digits.")
        elif not isbn.isnumeric():
            raise serializers.ValidationError("ISBN should be numeric.")

        pages = attrs.get('pages')
        if pages < 0:
            raise serializers.ValidationError("page should be greater than 0.")
        return attrs
    #
    # def validate_isbn(self, isbn: str):
    #     if BookModel.objects.filter(isbn=isbn).exists():
    #         raise serializers.ValidationError("This ISBN is already exists.")
    #     elif len(isbn) != 13:
    #         raise serializers.ValidationError("ISBN should be 13 digits.")
    #     elif not isbn.isnumeric():
    #         raise serializers.ValidationError("ISBN should be numeric.")
    #     return isbn

    def create(self, validated_data):
        return BookModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.content = validated_data.get('content', instance.content)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.subtitle = validated_data.get('subtitle', instance.subtitle)
        instance.pages = validated_data.get('pages')
        instance.in_stock = validated_data.get('in_stock')
        instance.save()
        return instance
