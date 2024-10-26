from django.test import TestCase
from django.urls import reverse
from .models import Restaurant, Pengumuman

class PengumumanModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Restoran A", location="Jl. Contoh No. 1")
        self.pengumuman = Pengumuman.objects.create(
            restaurant=self.restaurant, 
            judul="Promo Diskon", 
            konten="Dapatkan diskon 50% minggu ini!"
        )

    def test_pengumuman_creation(self):
        self.assertEqual(self.pengumuman.judul, "Promo Diskon")
        self.assertEqual(self.pengumuman.konten, "Dapatkan diskon 50% minggu ini!")
        self.assertEqual(self.pengumuman.restaurant.name, "Restoran A")
        self.assertIsNotNone(self.pengumuman.created_at)


class PengumumanViewsTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Restoran B", location="Jl. Contoh No. 2")
        self.pengumuman = Pengumuman.objects.create(
            restaurant=self.restaurant,
            judul="Pengumuman Liburan",
            konten="Restoran tutup selama liburan akhir tahun."
        )

    def test_daftar_pengumuman_view(self):
        response = self.client.get(reverse('daftar_pengumuman', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pengumuman.judul)

    def test_tambah_pengumuman_view_get(self):
        response = self.client.get(reverse('tambah_pengumuman', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tambah Pengumuman")

    def test_tambah_pengumuman_view_post(self):
        data = {
            'judul': 'Jam Operasional Baru',
            'konten': 'Kami buka lebih awal mulai minggu depan.'
        }
        response = self.client.post(reverse('tambah_pengumuman', args=[self.restaurant.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Pengumuman.objects.filter(judul="Jam Operasional Baru").exists())

    def test_detail_pengumuman_view(self):
        response = self.client.get(reverse('detail_pengumuman', args=[self.pengumuman.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pengumuman.judul)
        self.assertContains(response, self.pengumuman.konten)


