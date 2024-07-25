from django.core.management.base import BaseCommand
from django.db import transaction
from FavoriteURL.models import Category

class Command(BaseCommand):
    help = 'Category Delete'

    def add_arguments(self, parser):
        parser.add_argument('--id_category', type=str, required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        id_category = options.get('id_category', None)
        
        if id_category:
            category = Category.objects.get(id=id_category)
            category.delete()
        
            print('status:', "successfully")
        else:
            print('status:', "unsuccessfully")