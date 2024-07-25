from django.urls import path
from .views import FavoriteURL, CategoryClass, TagsClass, CheckUrls

urlpatterns = [
    path('favorite_url/', FavoriteURL.as_view(), name='favorite_url'),
    path('category/', CategoryClass.as_view(), name='category'),
    path('tags/', TagsClass.as_view(), name='tags'),
    path('check_urls/', CheckUrls.as_view(), name='check_urls'),
]
