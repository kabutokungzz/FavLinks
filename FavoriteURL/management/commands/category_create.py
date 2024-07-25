from django.core.management.base import BaseCommand
from django.db import transaction
from FavoriteURL.models import Category
from libs.get_one_query import first_query
class Command(BaseCommand):
    help = 'Category Create'

    def add_arguments(self, parser):
        parser.add_argument('--category', type=str, required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        category = options.get('category', None)
        mode = 'Create'
        category_objects = Category.objects.filter(type_name=category)
        if category_objects.exists():
            category_objects = first_query(category_objects)
            category_objects.type_name = category
            category_objects.save()
            mode = 'Update'
        else:
            category_objects = Category.objects.create(type_name=category)
            category_objects.save()
        
        print('mode: ', mode, ' status: ', "successfully")