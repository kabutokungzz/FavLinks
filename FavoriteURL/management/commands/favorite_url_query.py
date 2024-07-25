from django.core.management.base import BaseCommand
from decimal import *
from FavoriteURL.serializers import Favorite_UrlSerializer
from django.db.models import Q
from FavoriteURL.models import Favorite_Url
class Command(BaseCommand):
    help = 'Fetch Data Favorite_Url'

    def add_arguments(self, parser):
        parser.add_argument('--search_url', type=str, required=False)
        parser.add_argument('--search_category', type=str, required=False)
        parser.add_argument('--search_tags', type=str, required=False)

    def handle(self, *args, **options):
        search_url = options.get('search_url', None)
        search_category = options.get('search_category', None)
        search_tags = options.get('search_tags', None)
        
        favorite_url = Favorite_Url.objects.all()
        
        if search_url:
            favorite_url = favorite_url.filter(Q(url_favorite__icontains=search_url))

        if search_category:
            favorite_url = favorite_url.filter(Q(category__type_name__icontains=search_category))

        if search_tags:
            favorite_url = favorite_url.filter(Q(link_data__tags__tage_name__icontains=search_tags))
        
        serializer = Favorite_UrlSerializer(favorite_url , many=True)
        
        for value in serializer.data:
            print(value)