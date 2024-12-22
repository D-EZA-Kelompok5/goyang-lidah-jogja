import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goyang_lidah_jogja.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import UserProfile
from django.db import transaction

# Dictionary of users with their passwords
users_data = {
    'gordon.ramsay': 'ChefKing2024!', 
    'jamie.oliver': 'PastaMaster123!',
    'thomas.keller': 'FineDine@987',
    'nigella.lawson': 'SassyChef#21',
    'emeril.lagasse': 'BamEnergy!99',
    'wolfgang.puck': 'CuisineStar*88',
    'alice.waters': 'FarmToTable#1',
    'marco.pierre': 'LegendaryChef$7',
    'david.chang': 'RamenGuru123!',
    'anthony.bourdain': 'WanderCook*77',
    'rene.redzepi': 'NordicCuisine!22',
    'ferran.adria': 'AvantGarde#1',
    'massimobottura': 'ArtisanChef2023',
    'alain.ducasse': 'MichelinMagic*99',
    'heston.blumenthal': 'ScienceInFood#7',
    'eric.ripert': 'SeafoodSavant!98',
    'daniel.boulud': 'FrenchFlair#1',
    'nancy.silverton': 'BakerStar@20',
    'thomas.ina': 'SimplicityInFlavors*5',
    'marcus.samuelsson': 'GlobalFlavor@77'
}

@transaction.atomic
def create_users():
    print("Starting user creation...")
    
    # First, let's clean up any existing data
    print("Cleaning up existing data...")
    UserProfile.objects.all().delete()
    User.objects.all().delete()

    print(UserProfile.objects.count())
    print(User.objects.count())
    
    for username, password in users_data.items():
        try:
            # Check if user exists
            if User.objects.filter(username=username).exists():
                print(f"User {username} already exists, skipping...")
                continue
                
            # Create User instance
            user = User.objects.create_user(
                username=username,
                password=password,
                email=f"{username}@example.com"
            )
            
            # Check if profile exists
            if UserProfile.objects.filter(user=user).exists():
                print(f"Profile for {username} already exists, skipping...")
                continue
                
            # Create associated UserProfile
            UserProfile.objects.create(
                user=user,
                role='RESTAURANT_OWNER',
                bio='',
                profile_picture=None,
                review_count=0,
                level='BEGINNER'
            )
            
            print(f"Created user: {username}")
            
        except Exception as e:
            print(f"Error creating user {username}: {str(e)}")
            continue  # Continue with next user instead of raising

    print("User creation completed!")
    print(f"Total users created: {User.objects.count()}")
    print(f"Total profiles created: {UserProfile.objects.count()}")

if __name__ == "__main__":
    create_users()