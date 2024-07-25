from django.core.management.base import BaseCommand
from django.db import transaction
from FavoriteURL.models import Favorite_Url 

class Command(BaseCommand):
    help = 'Favorite_Url Delete'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=str, required=True , help='Id Favorite_Url')

    @transaction.atomic
    def handle(self, *args, **options):
        id_favorite = options.get('id', None)
        
        status_update = 'unsuccessfully'
        if id_favorite:
            favorite_url = Favorite_Url.objects.select_for_update().get(id=id_favorite)
            favorite_url.delete()
        
            print('status: ', status_update)
        else:
            print('status: ', status_update)