from django.core.management.base import BaseCommand
from django.db import transaction
from FavoriteURL.models import Favorite_Url
from libs.link_category_or_tags import link_category_or_tags
from libs.get_one_query import first_query

class Command(BaseCommand):
    help = 'Favorite_Url Create'

    def add_arguments(self, parser):
        parser.add_argument('--url_favorite', type=str, required=True)
        parser.add_argument('--category', type=str, required=False)
        parser.add_argument('--tags', type=str, required=False)

    @transaction.atomic
    def handle(self, *args, **options):
        url_favorite = options.get('url_favorite', None)
        category = options.get('search_category', None)
        tags = options.get('tags', None)
        
        mode = 'Create'
        favorite_Url_objects = Favorite_Url.objects.select_for_update().filter(url_favorite=url_favorite)
        if favorite_Url_objects.exists():
            favorite_Url_objects = first_query(favorite_Url_objects)
            favorite_Url_objects = url_favorite
            favorite_Url_objects.save()
            mode = 'Update'
        else:
            favorite_Url_objects = Favorite_Url.objects.create(
                url_favorite=url_favorite
            )
            favorite_Url_objects.save()

        status_update = link_category_or_tags(category, tags, favorite_Url_objects)
        
        print('mode: ', mode, ' status: ', status_update)