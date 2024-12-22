import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goyang_lidah_jogja.settings')
django.setup()

from django.db import transaction
from menuResto.models import Menu
from userPreferences.models import Tag, MenuTag

# Tag data with associated menu IDs
tag_data = {
    'Beverages': [5, 24, 29, 30, 58, 44, 45, 50],
    'Coffee & Tea': [9, 10, 19, 20, 33, 52],
    'Cold Drinks': [5, 24, 29, 30, 58, 50],
    'Fusion': [22, 23, 54, 49],
    'Grilled/BBQ': [65, 64, 99, 53, 63],
    'Healthy/Fresh': [32, 59, 60, 50, 42, 57, 56],
    'Hot Drinks': [10, 19, 20, 25, 44, 52, 9],
    'Javanese Cuisine': [67, 68, 69, 70, 91, 92, 93, 94, 95, 40, 86, 87, 61, 81, 36],
    'Local Indonesian': [1, 3, 11, 12, 13, 14, 15, 34, 64, 39, 61, 67, 68, 69, 70, 91, 92, 93, 94, 95],
    'Noodles': [35, 36, 37, 78, 79],
    'Pizza & Pasta': [6, 7, 8, 16, 17, 18],
    'Poultry': [1, 2, 11, 15, 21, 26, 39, 46, 51, 62, 64, 65, 69, 70, 71, 83, 84, 85, 4, 66, 68, 69, 70, 81, 82, 84, 85],
    'Rice Dishes': [34, 64, 40, 80, 91, 92, 93, 94, 95, 64],
    'Satay/Skewered': [71, 72, 73, 83],
    'Seafood': [12, 47, 48, 90, 97, 98, 96, 99, 100],
    'Soups & Stews': [28, 41, 46, 37, 85, 77],
    'Spicy': [11, 12, 15, 39, 100],
    'Street Food Style': [71, 72, 73, 86, 87, 88, 89, 13, 14],
    'Vegetarian/Vegan': [13, 31, 32, 56, 57, 59, 60, 61, 88, 86, 87],
    'Western': [6, 7, 8, 16, 17, 23, 55]
}

@transaction.atomic
def populate_tags():
    print("Starting tag creation and menu associations...")
    
    try:
        # First, create all tags
        for tag_name in tag_data.keys():
            tag, created = Tag.objects.get_or_create(name=tag_name)
            status = "Created" if created else "Already exists"
            print(f"{status}: Tag '{tag_name}'")
        
        # Then create all menu associations
        association_count = 0
        for tag_name, menu_ids in tag_data.items():
            tag = Tag.objects.get(name=tag_name)
            
            for menu_id in menu_ids:
                try:
                    menu = Menu.objects.get(id=menu_id)
                    # Create the association using the through model
                    MenuTag.objects.get_or_create(
                        tag=tag,
                        menu=menu
                    )
                    association_count += 1
                except Menu.DoesNotExist:
                    print(f"Warning: Menu with ID {menu_id} does not exist")
                except Exception as e:
                    print(f"Error associating menu {menu_id} with tag '{tag_name}': {str(e)}")
        
        print(f"\nTag population completed successfully!")
        print(f"Created {Tag.objects.count()} tags")
        print(f"Created {association_count} menu-tag associations")
            
    except Exception as e:
        print(f"Error during tag population: {str(e)}")
        raise

if __name__ == "__main__":
    populate_tags()