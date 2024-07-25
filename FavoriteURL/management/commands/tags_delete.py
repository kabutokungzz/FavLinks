from django.core.management.base import BaseCommand
from django.db import transaction
from FavoriteURL.models import Tags
class Command(BaseCommand):
    help = 'Tags Delete'

    def add_arguments(self, parser):
        parser.add_argument('--id_tag', type=str, required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        id_tag = options.get('id_tag', None)
        if id_tag:
            tags = Tags.objects.get(id=id_tag)
            tags.delete()
            print('status:', "successfully")
        else:
            print('status:', "unsuccessfully")