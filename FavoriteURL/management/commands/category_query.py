from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db import transaction

from FavoriteURL.serializers import CategorySerializer

from FavoriteURL.models import Category 

class Command(BaseCommand):
    help = 'Fetch Data Category'

    def add_arguments(self, parser):
        parser.add_argument('--search_category', type=str, required=False)
        parser.add_argument('--search_url', type=str, required=False)

    def handle(self, *args, **options):
        search_category = options.get('search_category', None)
        search_url = options.get('search_url', None)
        
        category = Category.objects.filter()
        if search_category:
            category = category.filter(Q(type_name__icontains=search_category))
            
        if search_url:
            category = category.filter(Q(favorite_url__url_favorite__icontains=search_url))
        
        serializer = CategorySerializer(category , many=True)
        for value in serializer.data:
            print(value)