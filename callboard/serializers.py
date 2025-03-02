from rest_framework import serializers

from callboard.models import Advertisement, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class AdvertisementSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Advertisement
        fields = ("title", "price", "description", "author", "created_at", "comments")
