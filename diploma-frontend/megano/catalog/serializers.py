from rest_framework import serializers

from .models import CatalogItem
from myauth.models import Avatar
from tags.models import Tag
from product.models import ProductShort, SaleItem, Review
from product.serializers import ReviewsSerializer


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["src", "alt"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class CategoriesSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = CatalogItem
        fields = ["id", "title", "image", "subcategories"]

    @staticmethod
    def get_subcategories(obj):
        subcategories = obj.subcategories.all()
        return CategoriesSerializer(subcategories, many=True).data


class CatalogSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewsSerializer(many=True, source="product_reviews")
    rating = serializers.SerializerMethodField()

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
            "rating",
        ]

    @staticmethod
    def get_reviews(obj):
        return obj.reviews.count()

    @staticmethod
    def get_rating(obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0


class SaleSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    price = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "price",
            "salePrice",
            "date_from",
            "date_to",
            "title",
            "images",
        ]

    @staticmethod
    def get_price(obj):
        return obj.price.price

    @staticmethod
    def get_title(obj):
        return obj.title.title
