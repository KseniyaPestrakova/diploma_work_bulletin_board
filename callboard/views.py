from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from callboard.models import Advertisement, Comment
from callboard.paginators import AdvertisementPaginator
from callboard.serializers import AdvertisementSerializer, CommentSerializer
from users.permissions import IsAdmin, IsAuthor


class AdvertisementCreateAPIView(generics.CreateAPIView):
    '''Представление для создания объявления. Только авторизованные пользователи могут создавать объявления.'''
    serializer_class = AdvertisementSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        '''Переопределённый метод для сохранения объявления с привязкой к текущему пользователю.'''
        ad = serializer.save()
        ad.author = self.request.user
        ad.save()


class AdvertisementListAPIView(generics.ListAPIView):
    '''Представление для получения списка всех объявлений с возможностью фильтрации и сортировки.'''
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    permission_classes = [AllowAny]
    pagination_class = AdvertisementPaginator
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("title",)
    ordering_fields = ("created_at",)


class AdvertisementRetrieveAPIView(generics.RetrieveAPIView):
    '''Представление для получения подробной информации об объявлении.'''
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]


class AdvertisementUpdateAPIView(generics.UpdateAPIView):
    '''Представление для обновления объявления.'''
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]


class AdvertisementDestroyAPIView(generics.DestroyAPIView):
    '''Представление для удаления объявления.'''
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]


class CommentCreateAPIView(generics.CreateAPIView):
    '''Представление для создания комментария под объявлением.'''
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        '''Переопределённый метод для сохранения комментария с привязкой к текущему пользователю.'''
        ad = serializer.save()
        ad.author = self.request.user
        ad.save()


class CommentListAPIView(generics.ListAPIView):
    '''Представление для получения списка комментариев.'''
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]


class CommentRetrieveAPIView(generics.RetrieveAPIView):
    '''Представление для получения подробной информации о комментарии.'''
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]


class CommentUpdateAPIView(generics.UpdateAPIView):
    '''Представление для обновления комментария.'''
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]


class CommentDestroyAPIView(generics.DestroyAPIView):
    '''Представление для удаления комментария.'''
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsAuthor]
