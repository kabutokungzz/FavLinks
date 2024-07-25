import jwt , re , string , random , json , math , requests , datetime
from django.views import View
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from json import loads
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login , logout 
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from FavoriteURL.models import Favorite_Url, Category, Tags, LinkData , CheckUrlsLog

from FavoriteURL.serializers import Favorite_UrlSerializer, CategorySerializer, LinkDataSerializer , TagsSerializer
from libs.pagination_cal import pagination_cal
from libs.link_category_or_tags import link_category_or_tags
from libs.get_one_query import first_query
# 3. Add Favorite URL
# 4. Manage Favorite URL
# 6. Search and Filter Favorites
@method_decorator(csrf_exempt, name='dispatch')
class FavoriteURL(LoginRequiredMixin , View):
    login_url = "/login"
    def get(self, request):
        search_url = request.GET.get('search_url') or None
        search_category = request.GET.get('search_category') or None
        search_tags = request.GET.get('search_tags') or None
        
        # 7. URL Validity Check
        #Do FirstTime at Day
        # if not CheckUrlsLog.objects.filter(datecheck=datetime.datetime.now().date()):
        #     CheckUrlsLog(
        #         datecheck=datetime.datetime.now().date()
        #     ).save()
        #     requests.get("http://localhost:"+request.META['SERVER_PORT']+"/api/check_urls", timeout=120)
            
        #Pagination
        index_first = request.GET.get('index_first',False) or 0
        index_last = request.GET.get('index_last',False) or 0
        
        favorite_url = Favorite_Url.objects.all()
        
        if search_url:
            favorite_url = favorite_url.filter(Q(url_favorite__icontains=search_url))

        if search_category:
            favorite_url = favorite_url.filter(Q(category__type_name__icontains=search_category))

        if search_tags:
            favorite_url = favorite_url.filter(Q(link_data__tags__tage_name__icontains=search_tags))
        
        totalCount, pagesCount, pagesSize, favorite_url = pagination_cal(index_first , index_last , favorite_url)
        
        serializer = Favorite_UrlSerializer(favorite_url , many=True)
        
        return JsonResponse({
            'data':serializer.data ,
            'totalCount':totalCount,
            'pagesSize':int(pagesSize),
            'pagesCount':pagesCount,
            'error': False,
        })
    
    # 8. Synchronization between User Actions and URL Validity Check 
    # I Add transaction.atomic and select_for_update When create and unique Tags and Category 
    @transaction.atomic
    def post(self, request):
        
        mode = 'Create'
        url_favorite = request.POST.get('url_favorite')
        category = request.POST.get('category') or None
        tags = request.POST.get('tags') or None
            
        favorite_Url_objects = Favorite_Url.objects.select_for_update().filter(url_favorite=url_favorite)
        if favorite_Url_objects.exists():
            favorite_Url_objects = first_query(favorite_Url_objects)
            favorite_Url_objects = url_favorite
            favorite_Url_objects.save()
            mode = 'Update'
        else:
            favorite_Url_objects = Favorite_Url.objects.create(
                url_favorite=url_favorite
            )
            favorite_Url_objects.save()

        status_update = link_category_or_tags(category, tags, favorite_Url_objects)

        return JsonResponse({'mode': mode, 'status': status_update})

    # 4. Manage Favorite URL
    @transaction.atomic
    def put(self, request):
        id_favorite = request.GET.get('id') or None
        body = json.loads(request.body)
        category = body.get('category') or None
        tags = body.get('tags') or None
        
        if id_favorite:
            favorite_url = Favorite_Url.objects.select_for_update().get(id=id_favorite)
            
            status_update = link_category_or_tags(category, tags, favorite_url)
            return JsonResponse({'status': status_update})
        return JsonResponse({'status': 'unsuccessfully'})
    
    @transaction.atomic
    def patch(self, request):
        id_favorite = request.GET.get('id') or None
        body = json.loads(request.body)
        
        if id_favorite:
            favorite_url = Favorite_Url.objects.select_for_update().get(id=id_favorite)
            favorite_url.url_favorite = body.get('url_favorite')
            favorite_url.save()

            return JsonResponse({'status': 'successfully'})
        return JsonResponse({'status': 'unsuccessfully'})

    @transaction.atomic
    def delete(self, request):
        id_favorite = request.GET.get('id') or None
        
        if id_favorite:
            favorite_url = Favorite_Url.objects.select_for_update().get(id=id_favorite)
            favorite_url.delete()
            
            return JsonResponse({'status': 'successfully'})
        return JsonResponse({'status': 'unsuccessfully'})


# 5.  Manage Category and Tag
# 6. Search and Filter Favorites
@method_decorator(csrf_exempt, name='dispatch')
class CategoryClass(LoginRequiredMixin , View):
    login_url = "/login"

    def get(self, request):
        search_category = request.GET.get('search_category') or None
        search_url = request.GET.get('search_url') or None
        
        #Pagination
        index_first = request.GET.get('index_first',False) or 0
        index_last = request.GET.get('index_last',False) or 0

        category = Category.objects.filter()
        if search_category:
            category = category.filter(Q(type_name__icontains=search_category))
            
        if search_url:
            category = category.filter(Q(favorite_url__url_favorite__icontains=search_url))
        
        totalCount, pagesCount, pageSize, category = pagination_cal(index_first , index_last , category)
        
        serializer = CategorySerializer(category , many=True)
        
        return JsonResponse({
            'data':serializer.data,
            'totalCount':totalCount,
            'pagesSize':int(pageSize),
            'pagesCount':pagesCount,
            'error': False})
    
    @transaction.atomic
    def post(self, request):
        
        mode = 'Create'
        category = request.POST.get('category')
        category_objects = Category.objects.filter(type_name=category)
        if category_objects.exists():
            category_objects = first_query(category_objects)
            category_objects.type_name = category
            category_objects.save()
            mode = 'Update'
        else:
            category_objects = Category.objects.create(type_name=category)
            category_objects.save()
            
        return JsonResponse({'mode': mode, 'status': 'successfully'})
    
    @transaction.atomic
    def patch(self, request):
        id_category = request.GET.get('id') or None
        body = json.loads(request.body)
        category = body.get('category') or None
        
        if id_category and category:
            category_object = Category.objects.get(id=id_category)
            category_object.type_name = category
            category_object.save()
            return JsonResponse({'status': 'Update Category successfully'})
        return JsonResponse({'status': 'Update Category unsuccessfully'})

    @transaction.atomic
    def delete(self, request):
        id_category = request.GET.get('id') or None
        if id_category:
            category = Category.objects.get(id=id_category)
            category.delete()
            
            return JsonResponse({'status': 'Delete Category successfully'})
        return JsonResponse({'status': 'Delete Category unsuccessfully'})


@method_decorator(csrf_exempt, name='dispatch')
class TagsClass(LoginRequiredMixin , View):
    login_url = "/login"

    def get(self, request):


        search_url = request.GET.get('search_url') or None
        search_tags = request.GET.get('search_tags') or None
        
        #Pagination
        index_first = request.GET.get('index_first',False) or 0
        index_last = request.GET.get('index_last',False) or 0
        
        tag = Tags.objects.filter()


        if search_tags:
            tag = tag.filter(Q(tage_name__icontains=search_tags))
            
        if search_url:
            tag = tag.filter(Q(link_data__favorite_url__url_favorite__icontains=search_url))

        
        totalCount, pagesCount, pageSize, tag = pagination_cal(index_first , index_last , tag)

        serializer = TagsSerializer(tag , many=True)
        
        return JsonResponse({
            'data':serializer.data,
            'totalCount':totalCount,
            'pagesSize':int(pageSize),
            'pagesCount':pagesCount,
            'error': False
        })
    
    @transaction.atomic
    def post(self, request):
        
        mode = 'Create'
        tag = request.POST.get('tag')
        tags_objects = Tags.objects.filter(tage_name=tag)
        if tags_objects.exists():
            tags_objects = first_query(tags_objects)
            tags_objects.tage_name = tag
            tags_objects.save()
            mode = 'Update'
        else:
            tags_objects = Tags.objects.create(tage_name=tag)
            tags_objects.save()
            
        return JsonResponse({'mode': mode, 'status': 'successfully'})
    
    @transaction.atomic
    def patch(self, request):
        id_tag = request.GET.get('id') or None
        body = json.loads(request.body)
        tag = body.get('tag') or None
        
        if id_tag and tag:
            tags_objects = Tags.objects.get(id=id_tag)
            tags_objects.tage_name = tag
            tags_objects.save()
            return JsonResponse({'status': 'Update Tag successfully'})
        return JsonResponse({'status': 'Update Tag unsuccessfully'})

    @transaction.atomic
    def delete(self, request):
        id_tag = request.GET.get('id') or None
        if id_tag:
            tags = Tags.objects.get(id=id_tag)
            tags.delete()
            
            return JsonResponse({'status': 'Delete Tag successfully'})
        return JsonResponse({'status': 'Delete Tag unsuccessfully'})

# 7. URL Validity Check
class CheckUrls(View):
    def get(self, request):
        favorite_url = Favorite_Url.objects.all()
        for favorite in favorite_url:
            try:
                requests.head(str(favorite.url_favorite), timeout=5)
                favorite.status = "valid"
            except requests.RequestException:
                favorite.status = "invalid"
            favorite.save()
        return JsonResponse({'status': 'Check Urls successfully'})