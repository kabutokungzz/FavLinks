from django.core.management.base import BaseCommand
from FavoriteURL.serializers import  TagsSerializer
from FavoriteURL.models import Tags
from django.db.models import Q

class Command(BaseCommand):
    help = 'Fetch Data Tags'

    def add_arguments(self, parser):
        parser.add_argument('--search_url', type=str, required=False)
        parser.add_argument('--search_tags', type=str, required=False)

    def handle(self, *args, **options):
        search_url = options.get('search_url', None)
        search_tags = options.get('search_tags', None)
        
        tag = Tags.objects.filter()
        if search_tags:
            tag = tag.filter(Q(tage_name__icontains=search_tags))
        if search_url:
            tag = tag.filter(Q(link_data__favorite_url__url_favorite__icontains=search_url))


        serializer = TagsSerializer(tag , many=True)
        for value in serializer.data:
            print(value)