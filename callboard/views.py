from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from callboard.models import Advertisement, Comment
from callboard.paginators import AdvertisementPaginator
from callboard.serializers import AdvertisementSerializer, CommentSerializer
from users.permissions import IsAdmin, IsAuthor


class AdvertisementCreateAPIView(generics.CreateAPIView):
    serializer_class = AdvertisementSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        ad = serializer.save()
        ad.author = self.request.user
        ad.save()


class AdvertisementListAPIView(generics.ListAPIView):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    permission_classes = [AllowAny]
    pagination_class = AdvertisementPaginator
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("title",)
    ordering_fields = ("created_at",)


class AdvertisementRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]


class AdvertisementUpdateAPIView(generics.UpdateAPIView):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]


class AdvertisementDestroyAPIView(generics.DestroyAPIView):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        ad = serializer.save()
        ad.author = self.request.user
        ad.save()


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]


class CommentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]


class CommentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]


class CommentDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]
