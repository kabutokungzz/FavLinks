from django.contrib import admin

from FavoriteURL.models import Favorite_Url, Category , Tags , LinkData



admin.site.register(Favorite_Url)
admin.site.register(Category)
admin.site.register(Tags)

admin.site.register(LinkData)