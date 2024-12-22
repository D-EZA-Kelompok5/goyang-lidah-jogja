import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goyang_lidah_jogja.settings')
django.setup()

from django.db import transaction
from main.models import Restaurant
from main.models import UserProfile

# Restaurant data updated with new image URLs
restaurant_data = [
    (1, 'Kesuma Restaurant', 'Restoran tradisional yang menyajikan cita rasa asli Indonesia dengan suasana khas Jogja. Terkenal dengan bumbu rempah aromatis dan masakan rumahan.', 'Gang Sartono, 829 Mantrijeron III, Yogyakarta 55143 Indonesia', 'Indonesia', '$$ - $$$', 'https://homestaydijogja.net/wp-content/uploads/2024/01/Kesuma-Restaurant-Yogyakarta.jpg', 1),
    
    (2, 'Mediterranea Restaurant by Kamil', 'Perpaduan elegan masakan Italia dan Prancis dengan sentuhan modern. Menyajikan hidangan Mediterania autentik yang disiapkan oleh koki berpengalaman.', 'Jl. Tirtodipuran No.24a, Yogyakarta 55143 Indonesia', 'Italia, Prancis', '$$ - $$$', 'https://static.promediateknologi.id/crop/0x0:0x0/750x500/photo/p1/1035/2023/12/06/Mediterranea-Restaurant-by-Kamil-cafe-unik-di-Jogja-yang-menyajikan-aneka-kuliner-khas-Mediterania-2593672500.jpeg', 2),
    
    (3, 'Omah Singo Stay & Resto', 'Restoran Jawa dengan suasana pedesaan yang asri. Menyajikan masakan lokal di tengah taman yang tenang, cocok untuk makan bersama keluarga.', 'Jl. Gunung Wangi, Bangkil, Srimulyo, Kec. Piyungan, Yogyakarta 55792 Indonesia', 'Indonesia', '$', 'https://cf.bstatic.com/xdata/images/hotel/max1024x768/401832032.jpg?k=3263518c7ff971c5001008800d30f2d5c8f105fee42961dcbc3ab55cf65ea80d&o=&hp=1', 3),
    
    (4, 'Nanamia Pizzeria', 'Pizzeria Italia asli yang menyajikan pizza bakar kayu dan pasta segar. Tempat favorit pecinta masakan Eropa di Yogyakarta.', 'Jl. Tirtodipuran No. 1, Yogyakarta 55143 Indonesia', 'Italia, Prancis', '$$ - $$$', 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/22/fb/df/00/nanamia-tirtodipuran.jpg?w=1200&h=-1&s=1', 4),
    
    (5, 'Tio Ciu Seafood & Chinese Food', 'Restoran Tionghoa ternama yang mengkhususkan diri dalam hidangan seafood dan masakan Cina tradisional. Terkenal dengan saus yang lezat dan bahan-bahan segar.', 'Jl. Jenderal Sudirman 23, Yogyakarta 55233 Indonesia', 'Cina', '$$ - $$$', 'https://media-cdn.tripadvisor.com/media/photo-s/09/3e/79/ee/photo0jpg.jpg', 5),
    
    (6, 'Viavia Jogja', 'Kafe-restoran menarik yang menyajikan masakan Indonesia klasik dengan pilihan vegetarian. Dilengkapi galeri seni dan ruang budaya.', 'Jl. Prawirotaman No.30 Brontokusuman, Mergangsan, Yogyakarta 55153 Indonesia', 'Indonesia', '$', 'https://media-cdn.tripadvisor.com/media/photo-s/19/e3/00/7f/viavia-resto-in-in-the.jpg', 6),
    
    (7, 'Water Castle Cafe', 'Kafe bersejarah dekat Taman Sari. Menyajikan minuman dan makanan ringan tradisional Jawa dalam suasana bangunan heritage.', 'Jl. Polowijan, Patehan, Yogyakarta 55133 Indonesia', 'Indonesia', '$', 'https://awsimages.detik.net.id/community/media/visual/2023/09/20/nostalgia-nuansa-tempo-dulu-di-water-castle-cafe-yogya_169.jpeg?w=1200', 7),
    
    (8, 'Bakmi Jowo mbah Gito', 'Terkenal dengan mie Jawa autentik yang dibuat dengan resep tradisional turun-temurun. Suasana sederhana dan homey.', 'Jl. Nyi Agengnis No.9 Rejowinangun, Kotagede, Yogyakarta 55171 Indonesia', 'Indonesia', '$', 'https://jogjakita.co.id/wp-content/uploads/2021/05/Bakmi-Jowo-Mbah-Gito2.jpg', 8),
    
    (9, 'Bale Raos', 'Restoran masakan Jawa Keraton yang menyajikan hidangan yang dulunya disiapkan untuk Kesultanan. Suasana makan mewah dalam setting tradisional keraton.', 'Jl. Magangan Kulon No.1, Yogyakarta 55131 Indonesia', 'Asia, Indonesia', '$$ - $$$', 'https://images.genpi.co/resize/1280x860-100/uploads/jogja/arsip/normal/2021/12/23/tampilan-depan-restoran-bale-raos-foto-instagrambaleraos-luji.webp', 9),
    
    (10, 'Sentosa Seafood & Chinese Food', 'Restoran seafood populer yang menyajikan hasil laut segar dengan teknik masak Tionghoa. Terkenal dengan pilihan seafood hidup.', 'Jl. Jenderal Sudirman 23, Yogyakarta 55233 Indonesia', 'Cina, Makanan Laut, Asia', '$$ - $$$', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMzJfYz3jBmUgv1A0E_4idfymZuffLKfpbJQ&s', 10),
    
    (11, 'Pengilon', 'Restoran fusion modern yang menggabungkan cita rasa Mediterania dan Asia. Pemandangan gunung yang indah dan suasana kontemporer.', 'Jl. Shinta No.8, Karang Mloko, Kec. Ngaglik, Kabupaten Sleman, Yogyakarta 55581 Indonesia', 'Internasional, Mediterania, Asia', '$$ - $$$', 'https://media.suara.com/pictures/970x544/2021/07/21/33450-pengilon.jpg', 11),
    
    (12, 'Akkar Juice Bar', 'Tempat yang fokus pada kesehatan dengan menyajikan jus segar, smoothies, dan makanan ringan. Tempat ideal untuk pencinta makanan sehat.', 'Jalan Taman Siswa, Yogyakarta 55281 Indonesia', 'Internasional, Makanan Sehat, Restoran bar', '$$ - $$$', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxSjE9JpQFy2ttdtnK_CYHFt_h7lYEfDhRAA&s', 12),
    
    (13, 'Warung Bu Ageng', 'Warung lokal favorit yang menyajikan masakan Indonesia homemade. Terkenal dengan resep Jawa autentik dan keramahan pelayanannya.', 'Jl. Tirtodipuran St No.13, Mantrijeron, Yogyakarta City, Special Region of Yogyakarta 55143', 'Asia, Indonesia', '$$ - $$$', 'https://assets-a1.kompasiana.com/statics/crawl/552a55ea6ea834f2248b4567.jpeg', 13),
    
    (14, 'Gudeg Yu Djum', 'Restoran gudeg ikonik di Yogyakarta yang telah berdiri sejak 1950. Menyajikan hidangan khas kota dengan resep warisan.', 'Jl. Wijilan No.167 Panembahan, Kraton, Yogyakarta 55131 Indonesia', 'Asia, Indonesia', '$$ - $$$', 'https://gudegyudjumpusat.com/wp-content/uploads/2018/07/gudeg-yu-djum-pusat-sheraton-slide.jpg', 14),
    
    (15, 'Sate Ayam Podomoro', 'Warung sate spesialis yang terkenal dengan sate ayam bakar sempurna dan bumbu kacang resep rahasia.', 'Jl. Mataram No.11, Yogyakarta 55213 Indonesia', 'Asia, Indonesia', '$', 'https://visitingjogja.jogjaprov.go.id/wp-content/uploads/2016/04/sate-podomoro-6.jpg', 15),
    
    (16, 'Warung Bakmi Ketandan', 'Warung mie bersejarah yang memadukan cita rasa Tionghoa dan Jawa. Terkenal dengan mie buatan tangan dan resep tradisionalnya.', 'Jl. Bhayangkara No.17, Yogyakarta 55261 Indonesia', 'Cina, Asia, Indonesia', '$$ - $$$', 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgv06fgAxas1TAL2ZIJjwrsZnBJ0c623UuxkTmkBZu2ILlHiJXwGr6CKS3zeZgM51mPGJbX0JZHiqQiBly9r96JWlde_6oetzhHF0jt263Ck2gM_hSujTwnoE1HO4MuBtDEKe0QNK8AWVM/s1600/DSCF3853.jpg', 16),
    
    (17, 'Bedhot Restaurant', 'Restoran Indonesia kontemporer yang menyajikan hidangan tradisional dengan penyajian modern. Populer di kalangan lokal dan wisatawan.', 'Jl. Sosrowijayan Wetan GT1 No.127, Yogyakarta 55271 Indonesia', 'Asia, Indonesia', '$$ - $$$', 'https://media-cdn.tripadvisor.com/media/photo-s/0d/02/12/6f/dsc-0051-largejpg.jpg', 17),
    
    (18, 'Lotek Gado-Gado Colombo Bu Bagyo Sagan', 'Warung legendaris yang mengkhususkan diri dalam lotek dan gado-gado. Terkenal dengan sayuran segar dan bumbu kacang spesial.', 'Jl. Sagan I no. 1 Terban, Gondokusuman, Yogyakarta 55223 Indonesia', 'Asia, Indonesia', '$', 'https://media-cdn.tripadvisor.com/media/photo-s/1a/ee/2e/cd/lotek-gado-gado-colombo.jpg', 18),
    
    (19, 'Gudeg Pawon', 'Warung gudeg tradisional yang memasak di dapur kayu bakar. Cita rasa asli Yogyakarta dalam suasana pedesaan.', 'Jl. Janturan 36-38, Veteran Warungboto, Umbulharjo, Yogyakarta 55164 Indonesia', 'Asia, Indonesia', '$', 'https://tripjogja.co.id/wp-content/uploads/2019/10/Jam-Buka-Gudeg-Pawon.jpg', 19),
    
    (20, 'Bale Timoho Resto', 'Restoran seafood luas dengan menu Asia yang beragam. Terkenal dengan pilihan seafood segar dan suasana yang ramah untuk keluarga.', 'Jl. IPDA Tut Harsono No. 58, Yogyakarta 55165 Indonesia', 'Makanan Laut, Asia', '$$ - $$$', 'https://static.promediateknologi.id/crop/0x0:0x0/750x500/webp/photo/p1/1035/2023/12/07/Bale-Timoho-Resto-rekomendasi-tempat-makan-keluarga-di-Jogja-yang-menyajikan-aneka-kuliner-gurame-673124046.jpg', 20)
]

# Rest of the code remains the same
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