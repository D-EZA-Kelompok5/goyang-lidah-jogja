from django.test import TestCase
from django.urls import reverse
from .models import Restaurant, Pengumuman

class RestaurantAnnouncementModelTest(TestCase):
    def setUp(self):
        # Membuat objek Restaurant dan Pengumuman untuk digunakan dalam setiap test
        self.restaurant = Restaurant.objects.create(name="Restoran A", location="Jl. Contoh No. 1")
        self.pengumuman = Pengumuman.objects.create(
            restaurant=self.restaurant,
            judul="Promo Diskon",
            konten="Dapatkan diskon 50% minggu ini!"
        )

    def test_pengumuman_creation(self):
        """Test untuk memastikan pengumuman dibuat dengan benar"""
        self.assertEqual(self.pengumuman.judul, "Promo Diskon")
        self.assertEqual(self.pengumuman.konten, "Dapatkan diskon 50% minggu ini!")
        self.assertEqual(self.pengumuman.restaurant, self.restaurant)
        self.assertIsNotNone(self.pengumuman.created_at)

class RestaurantAnnouncementViewsTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Restoran B", location="Jl. Contoh No. 2")
        self.pengumuman = Pengumuman.objects.create(
            restaurant=self.restaurant,
            judul="Pengumuman Liburan",
            konten="Restoran tutup selama liburan akhir tahun."
        )

    def test_daftar_pengumuman_view(self):
        """Test untuk memastikan tampilan daftar pengumuman restoran bekerja"""
        response = self.client.get(reverse('daftar_pengumuman', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pengumuman.judul)
        self.assertTemplateUsed(response, 'daftar_pengumuman.html')

    def test_tambah_pengumuman_view_get(self):
        """Test untuk memastikan halaman tambah pengumuman tampil dengan benar"""
        response = self.client.get(reverse('tambah_pengumuman', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tambah Pengumuman")
        self.assertTemplateUsed(response, 'tambah_pengumuman.html')

    def test_tambah_pengumuman_view_post(self):
        """Test untuk memastikan pengumuman baru bisa ditambahkan melalui POST"""
        data = {
            'judul': 'Jam Operasional Baru',
            'konten': 'Kami buka lebih awal mulai minggu depan.'
        }
        response = self.client.post(reverse('tambah_pengumuman', args=[self.restaurant.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirect setelah sukses
        self.assertTrue(Pengumuman.objects.filter(judul="Jam Operasional Baru").exists())

    def test_detail_pengumuman_view(self):
        """Test untuk memastikan detail pengumuman ditampilkan dengan benar"""
        response = self.client.get(reverse('detail_pengumuman', args=[self.pengumuman.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pengumuman.judul)
        self.assertContains(response, self.pengumuman.konten)
        self.assertTemplateUsed(response, 'detail_pengumuman.html')
