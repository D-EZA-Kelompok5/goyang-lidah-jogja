from django.contrib import admin
from .models import Review, Menu

# Pendaftaran model sederhana
admin.site.register(Menu)

# Konfigurasi admin untuk Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu', 'rating', 'created_at')  # Kolom yang tampil di daftar
    list_filter = ('rating', 'created_at')  # Filter di sidebar admin
    search_fields = ('user__username', 'menu__name')  # Fitur pencarian
    ordering = ('-created_at',)  # Mengurutkan berdasarkan tanggal