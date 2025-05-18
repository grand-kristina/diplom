from rest_framework import serializers

from .models import ProductShort, Review, Specification
from myauth.models import Avatar
from tags.models import Tag


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["src", "alt"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ["name", "value"]


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "author",
            "email",
            "rate",
            "text",
            "date",
        ]

    @staticmethod
    def get_author(obj):
        return obj.author.username

    @staticmethod
    def get_email(obj):
        return obj.author.email

    @staticmethod
    def get_date(obj):
        return obj.date.strftime("%Y-%m-%d %H:%M")


class CreateReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "author",
            "rate",
            "text",
            "product",
        ]
        extra_kwargs = {
            "author": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context["request"].user

        review = Review.objects.create(author=user, **validated_data)

        return review


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    specifications = SpecificationsSerializer(many=True)
    reviews = ReviewsSerializer(many=True, source="product_reviews")
    title = serializers.SerializerMethodField()

    class Meta:
        model = ProductShort
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]
    
    @staticmethod
    def get_title(obj):
        print(obj.title[:3])
        return obj.title[:3]

    @staticmethod
    def get_reviews(obj):
        return obj.reviews.all()

    @staticmethod
    def get_rating(obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rate for review in reviews) / len(reviews)
        return 0

    @staticmethod
    def get_specifications(obj):
        return obj.specifications.all()
