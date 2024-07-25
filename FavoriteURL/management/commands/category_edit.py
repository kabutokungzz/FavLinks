from django.core.management.base import BaseCommand
from django.db import transaction
from FavoriteURL.models import Category

class Command(BaseCommand):
    help = 'Category Edit'

    def add_arguments(self, parser):
        parser.add_argument('--id_category', type=str, required=True)
        parser.add_argument('--category', type=str, required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        id_category = options.get('id_category', None)
        category = options.get('category', None)
        
        if id_category and category:
            category_object = Category.objects.get(id=id_category)
            category_object.type_name = category
            category_object.save()
        
        print('status:', "successfully")