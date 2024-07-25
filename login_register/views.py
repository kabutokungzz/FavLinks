import jwt , re , string , random
from django.views import View
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from json import loads
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth import login , logout 
from django.contrib.auth import authenticate

from django.contrib.auth.forms import UserCreationForm
from libs.get_one_query import first_query
# 1. User Registration
# 2. User Login

@method_decorator(csrf_exempt, name='dispatch')
class Login(View):

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request, 
            username=username, 
            password=password
        )
        if user is not None:
            login(request, user)
            return JsonResponse({'error': False, 'user_id': user.id})
        else:
            return JsonResponse({'error': True, 'user_id': user.id})
    


@method_decorator(csrf_exempt, name='dispatch')
class Logout(View):

    def post(self, request):
        logout(request)
        return JsonResponse({'logout': True})

@method_decorator(csrf_exempt, name='dispatch')
class Register(View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if username and password and email:
            
            if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
                return JsonResponse({'register': False, 'error': 'Password must be at least 8 characters and should have uppercase and lowercase characters.'})
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'register': False, 'error': 'There User in the system.'})
            elif User.objects.filter(email=email).exists():
                return JsonResponse({'register': False, 'error': 'Email already used'})
            else:
                user = User.objects.create_user(username=username, email=email , password=password)
                user.save()
                return JsonResponse({'register': True , 'error': ''})
        return JsonResponse({'register': False , 'error': ''}) 

@method_decorator(csrf_exempt, name='dispatch')
class ResetPassword(View):

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        newPassword = request.POST.get('newPassword')
        if username and email and newPassword:
            
            if len(newPassword) < 8 or not re.search(r'[A-Z]', newPassword) or not re.search(r'[a-z]', newPassword):
                return JsonResponse({'newPassWord': False, 'error': 'Password must be at least 8 characters and should have uppercase and lowercase characters.'})
            
            user = User.objects.filter(username=username , email=email)
            if user.exists():
                # newPass = ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))
                user = first_query(user)
                user.password = newPassword
                user.save()
                return JsonResponse({'newPassWord': 'successfully' , 'error': ''}) 
            
        return JsonResponse({'newPassWord': '' , 'error': 'User does not exist in the system or this email.'}) 