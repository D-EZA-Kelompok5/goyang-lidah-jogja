import os
import django
import csv
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goyang_lidah_jogja.settings')
django.setup()

from django.db import transaction
from main.models import Restaurant
from menuResto.models import Menu

@transaction.atomic
def populate_menus():
    print("Starting menu creation...")
    
    # Get the absolute path to the CSV file
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'menu_data.csv')
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            # Counter for successful entries
            success_count = 0
            
            for row in csv_reader:
                try:
                    # Get the restaurant instance
                    restaurant = Restaurant.objects.get(id=row['restaurant_id'])
                    
                    # Create the menu item
                    Menu.objects.create(
                        restaurant=restaurant,
                        name=row['name'],
                        description=row['description'],
                        price=int(float(row['price'])),  # Convert to integer if price is in decimal
                        image=row['image'] if row['image'] else None
                    )
                    
                    success_count += 1
                    if success_count % 10 == 0:  # Progress update every 10 items
                        print(f"Created {success_count} menu items...")
                        
                except Restaurant.DoesNotExist:
                    print(f"Error: Restaurant with ID {row['restaurant_id']} does not exist")
                except ValueError as ve:
                    print(f"Error with price conversion for menu '{row['name']}': {str(ve)}")
                except Exception as e:
                    print(f"Error creating menu '{row['name']}': {str(e)}")
                    continue
            
            print(f"\nMenu creation completed successfully!")
            print(f"Total menu items created: {success_count}")
            
    except FileNotFoundError:
        print(f"Error: Could not find menu_data.csv at {csv_path}")
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")

if __name__ == "__main__":
    populate_menus()