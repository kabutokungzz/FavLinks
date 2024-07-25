from rest_framework import serializers
from FavoriteURL.models import Category , Tags , Favorite_Url , LinkData


        
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'tage_name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'type_name')

class LinkDataSerializer(serializers.ModelSerializer):
    # favorite_url = Favorite_UrlSerializer()
    tags = TagsSerializer()
    class Meta:
        model = LinkData
        fields = ('id' , 'tags')

class Favorite_UrlSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    link_data = LinkDataSerializer(many=True)
    class Meta:
        model = Favorite_Url
        fields = ('id', 'url_favorite', 'status', 'category' , 'link_data')

