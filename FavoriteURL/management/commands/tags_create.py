from django.core.management.base import BaseCommand
from django.db import transaction
from FavoriteURL.models import Tags 
from libs.get_one_query import first_query

class Command(BaseCommand):
    help = 'Tags Create'

    def add_arguments(self, parser):
        parser.add_argument('--tag', type=str, required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        tag = options.get('tag', None)
        mode = 'Create'
        tags_objects = Tags.objects.filter(tage_name=tag)
        if tag:
            if tags_objects.exists():
                tags_objects = first_query(tags_objects)
                tags_objects.tage_name = tag
                tags_objects.save()
                mode = 'Update'
            else:
                tags_objects = Tags.objects.create(tage_name=tag)
                tags_objects.save()
        
            print('status:', "successfully")
        else:
            print('status:', "unsuccessfully")