from django.core.management.base import BaseCommand
from django.db import transaction
from FavoriteURL.models import Favorite_Url
from libs.link_category_or_tags import link_category_or_tags

class Command(BaseCommand):
    help = 'Favorite_Url Edit'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=str, required=True , help='Id Favorite_Url')
        parser.add_argument('--url_change', type=str, required=False , help='new url for update')
        parser.add_argument('--category', type=str, required=False)
        parser.add_argument('--tags', type=str, required=False)

    @transaction.atomic
    def handle(self, *args, **options):
        id_favorite = options.get('id', None)
        url_chagne = options.get('url_change', None)
        category = options.get('category', None)
        tags = options.get('tags', None)
        
        status_update = 'unsuccessfully'
        if id_favorite:
            favorite_url = Favorite_Url.objects.select_for_update().get(id=id_favorite)
            if url_chagne:
                favorite_url.url_favorite = url_chagne
                favorite_url.save()
            status_update = link_category_or_tags(category, tags, favorite_url)
        
            print('status: ', status_update)
        else:
            print('status: ', status_update)