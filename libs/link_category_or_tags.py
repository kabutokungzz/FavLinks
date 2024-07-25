from FavoriteURL.models import Category, Tags, LinkData

def link_category_or_tags(category, tags, favorite_Url):
    if category:
        category , category_create_ = Category.objects.get_or_create(type_name=category)
        if category_create_:
            category.save()
            
        favorite_Url.category = category
        favorite_Url.save()
            
    if tags:
        tags , tags_create = Tags.objects.get_or_create(tage_name=tags)
        if tags:
            if tags_create:
                tags.save()
        link_data, link_create = LinkData.objects.get_or_create(
            favorite_url=favorite_Url,
            tags=tags,
        )
        if link_create:
            link_data.save()
            
    return "successfully"