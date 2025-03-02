from django.urls import path

from callboard.apps import CallboardConfig
from callboard.views import (AdvertisementCreateAPIView, AdvertisementDestroyAPIView, AdvertisementListAPIView,
                             AdvertisementRetrieveAPIView, AdvertisementUpdateAPIView, CommentCreateAPIView,
                             CommentDestroyAPIView, CommentListAPIView, CommentRetrieveAPIView, CommentUpdateAPIView)

app_name = CallboardConfig.name


urlpatterns = [
    path("ad/create/", AdvertisementCreateAPIView.as_view(), name="ad-create"),
    path("ad/", AdvertisementListAPIView.as_view(), name="ad-list"),
    path("ad/<int:pk>/", AdvertisementRetrieveAPIView.as_view(), name="ad-get"),
    path("ad/update/<int:pk>/", AdvertisementUpdateAPIView.as_view(), name="ad-update"),
    path("ad/delete/<int:pk>/", AdvertisementDestroyAPIView.as_view(), name="ad-delete"),
    path("comment/create/", CommentCreateAPIView.as_view(), name="comment-create"),
    path("comment/", CommentListAPIView.as_view(), name="comment-list"),
    path("comment/<int:pk>/", CommentRetrieveAPIView.as_view(), name="comment-get"),
    path("comment/update/<int:pk>/", CommentUpdateAPIView.as_view(), name="comment-update"),
    path("comment/delete/<int:pk>/", CommentDestroyAPIView.as_view(), name="comment-delete"),
]
