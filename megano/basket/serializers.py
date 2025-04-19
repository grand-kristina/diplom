from rest_framework import serializers

from myauth.models import Avatar
from tags.models import Tag
from product.models import ProductShort


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["src", "alt"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class BasketSerializers(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

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

    def get_count(self, obj):
        counts = self.context.get("counts", {})
        return counts.get(obj.id, 0)
