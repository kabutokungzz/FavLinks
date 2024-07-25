from django.core.management.base import BaseCommand
from django.db import transaction
from FavoriteURL.models import Tags

class Command(BaseCommand):
    help = 'Tags Edit'

    def add_arguments(self, parser):
        parser.add_argument('--id_tag', type=str, required=True)
        parser.add_argument('--tag', type=str, required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        id_tag = options.get('id_tag', None)
        tag = options.get('tag', None)
        
        if id_tag and tag:
            tags_objects = Tags.objects.get(id=id_tag)
            tags_objects.tage_name = tag
            tags_objects.save()
            print('status:', "successfully")
        else:
            print('status:', "unsuccessfully")