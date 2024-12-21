import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goyang_lidah_jogja.settings')
django.setup()

from django.db import transaction
from main.models import Restaurant
from authentication.models import UserProfile

# Restaurant data as a list of tuples
restaurant_data = [
    (1, 'Kesuma Restaurant', 'Restoran tradisional yang menyajikan cita rasa asli Indonesia dengan suasana khas Jogja. Terkenal dengan bumbu rempah aromatis dan masakan rumahan.', 'Gang Sartono, 829 Mantrijeron III, Yogyakarta 55143 Indonesia', 'Indonesia', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 1),
    
    (2, 'Mediterranea Restaurant by Kamil', 'Perpaduan elegan masakan Italia dan Prancis dengan sentuhan modern. Menyajikan hidangan Mediterania autentik yang disiapkan oleh koki berpengalaman.', 'Jl. Tirtodipuran No.24a, Yogyakarta 55143 Indonesia', 'Italia, Prancis', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 2),
    
    (3, 'Omah Singo Stay & Resto', 'Restoran Jawa dengan suasana pedesaan yang asri. Menyajikan masakan lokal di tengah taman yang tenang, cocok untuk makan bersama keluarga.', 'Jl. Gunung Wangi, Bangkil, Srimulyo, Kec. Piyungan, Yogyakarta 55792 Indonesia', 'Indonesia', '$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 3),
    
    (4, 'Nanamia Pizzeria', 'Pizzeria Italia asli yang menyajikan pizza bakar kayu dan pasta segar. Tempat favorit pecinta masakan Eropa di Yogyakarta.', 'Jl. Tirtodipuran No. 1, Yogyakarta 55143 Indonesia', 'Italia, Prancis', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 4),
    
    (5, 'Tio Ciu Seafood & Chinese Food', 'Restoran Tionghoa ternama yang mengkhususkan diri dalam hidangan seafood dan masakan Cina tradisional. Terkenal dengan saus yang lezat dan bahan-bahan segar.', 'Jl. Jenderal Sudirman 23, Yogyakarta 55233 Indonesia', 'Cina', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 5),
    
    (6, 'Viavia Jogja', 'Kafe-restoran menarik yang menyajikan masakan Indonesia klasik dengan pilihan vegetarian. Dilengkapi galeri seni dan ruang budaya.', 'Jl. Prawirotaman No.30 Brontokusuman, Mergangsan, Yogyakarta 55153 Indonesia', 'Indonesia', '$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 6),
    
    (7, 'Water Castle Cafe', 'Kafe bersejarah dekat Taman Sari. Menyajikan minuman dan makanan ringan tradisional Jawa dalam suasana bangunan heritage.', 'Jl. Polowijan, Patehan, Yogyakarta 55133 Indonesia', 'Indonesia', '$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 7),
    
    (8, 'Bakmi Jowo mbah Gito', 'Terkenal dengan mie Jawa autentik yang dibuat dengan resep tradisional turun-temurun. Suasana sederhana dan homey.', 'Jl. Nyi Agengnis No.9 Rejowinangun, Kotagede, Yogyakarta 55171 Indonesia', 'Indonesia', '$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 8),
    
    (9, 'Bale Raos', 'Restoran masakan Jawa Keraton yang menyajikan hidangan yang dulunya disiapkan untuk Kesultanan. Suasana makan mewah dalam setting tradisional keraton.', 'Jl. Magangan Kulon No.1, Yogyakarta 55131 Indonesia', 'Asia, Indonesia', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 9),
    
    (10, 'Sentosa Seafood & Chinese Food', 'Restoran seafood populer yang menyajikan hasil laut segar dengan teknik masak Tionghoa. Terkenal dengan pilihan seafood hidup.', 'Jl. Jenderal Sudirman 23, Yogyakarta 55233 Indonesia', 'Cina, Makanan Laut, Asia', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 10),
    
    (11, 'Pengilon', 'Restoran fusion modern yang menggabungkan cita rasa Mediterania dan Asia. Pemandangan gunung yang indah dan suasana kontemporer.', 'Jl. Shinta No.8, Karang Mloko, Kec. Ngaglik, Kabupaten Sleman, Yogyakarta 55581 Indonesia', 'Internasional, Mediterania, Asia', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 11),
    
    (12, 'Akkar Juice Bar', 'Tempat yang fokus pada kesehatan dengan menyajikan jus segar, smoothies, dan makanan ringan. Tempat ideal untuk pencinta makanan sehat.', 'Jalan Taman Siswa, Yogyakarta 55281 Indonesia', 'Internasional, Makanan Sehat, Restoran bar', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 12),
    
    (13, 'Warung Bu Ageng', 'Warung lokal favorit yang menyajikan masakan Indonesia homemade. Terkenal dengan resep Jawa autentik dan keramahan pelayanannya.', 'Jl. Tirtodipuran St No.13, Mantrijeron, Yogyakarta City, Special Region of Yogyakarta 55143', 'Asia, Indonesia', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 13),
    
    (14, 'Gudeg Yu Djum', 'Restoran gudeg ikonik di Yogyakarta yang telah berdiri sejak 1950. Menyajikan hidangan khas kota dengan resep warisan.', 'Jl. Wijilan No.167 Panembahan, Kraton, Yogyakarta 55131 Indonesia', 'Asia, Indonesia', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 14),
    
    (15, 'Sate Ayam Podomoro', 'Warung sate spesialis yang terkenal dengan sate ayam bakar sempurna dan bumbu kacang resep rahasia.', 'Jl. Mataram No.11, Yogyakarta 55213 Indonesia', 'Asia, Indonesia', '$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 15),
    
    (16, 'Warung Bakmi Ketandan', 'Warung mie bersejarah yang memadukan cita rasa Tionghoa dan Jawa. Terkenal dengan mie buatan tangan dan resep tradisionalnya.', 'Jl. Bhayangkara No.17, Yogyakarta 55261 Indonesia', 'Cina, Asia, Indonesia', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 16),
    
    (17, 'Bedhot Restaurant', 'Restoran Indonesia kontemporer yang menyajikan hidangan tradisional dengan penyajian modern. Populer di kalangan lokal dan wisatawan.', 'Jl. Sosrowijayan Wetan GT1 No.127, Yogyakarta 55271 Indonesia', 'Asia, Indonesia', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 17),
    
    (18, 'Lotek Gado-Gado Colombo Bu Bagyo Sagan', 'Warung legendaris yang mengkhususkan diri dalam lotek dan gado-gado. Terkenal dengan sayuran segar dan bumbu kacang spesial.', 'Jl. Sagan I no. 1 Terban, Gondokusuman, Yogyakarta 55223 Indonesia', 'Asia, Indonesia', '$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 18),
    
    (19, 'Gudeg Pawon', 'Warung gudeg tradisional yang memasak di dapur kayu bakar. Cita rasa asli Yogyakarta dalam suasana pedesaan.', 'Jl. Janturan 36-38, Veteran Warungboto, Umbulharjo, Yogyakarta 55164 Indonesia', 'Asia, Indonesia', '$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 19),
    
    (20, 'Bale Timoho Resto', 'Restoran seafood luas dengan menu Asia yang beragam. Terkenal dengan pilihan seafood segar dan suasana yang ramah untuk keluarga.', 'Jl. IPDA Tut Harsono No. 58, Yogyakarta 55165 Indonesia', 'Makanan Laut, Asia', '$$ - $$$', 'https://www.joglowisata.com/wp-content/uploads/2019/07/41947229_312587632868963_6585227879780083006_n-850x1024.jpg', 20)
]

@transaction.atomic
def populate_restaurants():
    print("Starting restaurant creation...")
    
    for (id, name, description, address, category, price_range, image, owner_id) in restaurant_data:
        try:
            # Get the owner (UserProfile) instance
            owner = UserProfile.objects.get(user_id=owner_id)
            
            # Create the restaurant
            restaurant = Restaurant.objects.create(
                name=name,
                description=description,
                address=address,
                category=category,
                price_range=price_range,
                image=image,
                owner=owner
            )
            
            print(f"Created restaurant: {name}")
            
        except UserProfile.DoesNotExist:
            print(f"Error: Owner with ID {owner_id} does not exist")
        except Exception as e:
            print(f"Error creating restaurant {name}: {str(e)}")
            raise

    print("Restaurant creation completed successfully!")

if __name__ == "__main__":
    populate_restaurants()