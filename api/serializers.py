from rest_framework import serializers
from .models import CustomUser, BookReview, BookHistory, Book


class BookHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookHistory
        fields = '__all__'


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    reviews = BookReviewSerializer(many=True, read_only=True)
    history = BookHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

        # thuộc tính này chỉ định đứa nào sẽ được ẩn đi

        extra_kwargs = {
            'password': {'write_only': True}
        }

    # we will hash it
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # nó kế thừa từ Model User nếu không giải ** thì sẽ yêu cầu thuộc tính ID ....
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
