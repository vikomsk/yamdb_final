from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from reviews.models import (ADMIN, ME, Category, Comment, Genre, Review, Title,
                            User)

CONFIRMATION_CODE_REQUIRED = {'confirmation_code': 'This field is required.'}
CONFIRMATION_CODE_INVALID = {'confirmation_code': 'This is an invalid value.'}
USERNAME_PROHIBITED = (
    'The {username} is prohibited.',
    'You should select another.'
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']


class UserMeSerializer(UserSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    def validate(self, data):
        instance = getattr(self, 'instance')
        if instance.role != ADMIN:
            data['role'] = instance.role
        return data


class UserSignUpSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, value):
        if value == ME:
            raise serializers.ValidationError(USERNAME_PROHIBITED)
        return value


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code', 'token']

    def validate(self, data):
        code = get_object_or_404(
            User, username=data['username']
        ).confirmation_code
        code_from_user = data.get('confirmation_code')
        if code_from_user is None:
            raise serializers.ValidationError(CONFIRMATION_CODE_REQUIRED)
        elif code != code_from_user:
            raise serializers.ValidationError(CONFIRMATION_CODE_INVALID)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    def validate_year(self, value):
        year = timezone.now().year
        if not (value <= year):
            raise serializers.ValidationError('Incorrectly year.')
        return value

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, review):
        if self.context['request'].method != 'POST':
            return review

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'You have already written a review for this work.'
            )
        return review

    def validate_score(self, score):
        if not 1 <= score <= 10:
            raise serializers.ValidationError(
                'The score must be from 1 to 10'
            )
        return score

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
