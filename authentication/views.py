# authentication/views.py

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from main.models import UserProfile
from django.contrib.auth.decorators import login_required

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali username atau kata sandi."
        }, status=401)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password1 = data.get('password1')
            password2 = data.get('password2')
            role = data.get('role', 'CUSTOMER')  # Default role ke 'CUSTOMER'

            # Validasi input
            if not username or not password1 or not password2:
                return JsonResponse({
                    "status": False,
                    "message": "All fields are required."
                }, status=400)

            # Cek apakah password cocok
            if password1 != password2:
                return JsonResponse({
                    "status": False,
                    "message": "Passwords do not match."
                }, status=400)
            
            # Cek apakah username sudah ada
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": False,
                    "message": "Username already exists."
                }, status=400)
            
            # Buat user baru
            user = User.objects.create_user(username=username, password=password1)
            user.save()

            # Update UserProfile yang dibuat oleh signal
            user_profile = user.profile
            user_profile.role = role
            user_profile.bio = ''  # Atur bio sesuai kebutuhan
            user_profile.profile_picture = None  # Atur gambar profil jika diperlukan
            user_profile.review_count = 0  # Atur jumlah ulasan
            user_profile.level = 'BEGINNER'  # Atur level awal
            user_profile.save()

            return JsonResponse({
                "username": user.username,
                "status": 'success',
                "message": "User created successfully!"
            }, status=200)
        
        except KeyError as e:
            return JsonResponse({
                "status": False,
                "message": f"Missing field: {str(e)}"
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            }, status=500)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
@login_required
def get_profile(request):
    if request.method != 'GET':
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
    
    user = request.user
    profile = user.profile

    # Serialize preferences
    preferences = list(profile.preferences.values('name'))

    user_profile_data = {
        "user_id": profile.user.id,
        "username": user.username,
        "email": user.email,
        "role": profile.role,
        "bio": profile.bio,
        "profile_picture": profile.profile_picture,
        "review_count": profile.review_count,
        "level": profile.level,
        "preferences": preferences,
    }

    return JsonResponse(user_profile_data, status=200)

@csrf_exempt
def logout(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout gagal."
        }, status=401)
