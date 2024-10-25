import django.core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(choices=[('EVENT_MANAGER', 'Event Manager'), ('RESTAURANT_OWNER', 'Restaurant Owner'), ('CUSTOMER', 'Customer')], default='CUSTOMER', max_length=20)),
                ('bio', models.TextField(blank=True)),
                ('profile_picture', models.URLField(blank=True, max_length=500, null=True, validators=[django.core.validators.URLValidator()])),
                ('review_count', models.PositiveIntegerField(default=0)),
                ('level', models.CharField(choices=[('BRONZE', 'Bronze'), ('SILVER', 'Silver'), ('GOLD', 'Gold')], default='BRONZE', max_length=10)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('address', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=100)),
                ('price_range', models.CharField(max_length=50)),
                ('image', models.URLField(blank=True, max_length=500, null=True, validators=[django.core.validators.URLValidator()])),
                ('owner', models.ForeignKey(limit_choices_to={'role': 'RESTAURANT_OWNER'}, on_delete=django.db.models.deletion.CASCADE, related_name='owned_restaurant', to='main.userprofile')),
            ],
            options={
                'verbose_name': 'Restaurant',
                'verbose_name_plural': 'Restaurants',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.URLField(blank=True, max_length=500, null=True, validators=[django.core.validators.URLValidator()])),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='main.restaurant')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=255)),
                ('entrance_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('image', models.URLField(blank=True, max_length=500, null=True, validators=[django.core.validators.URLValidator()])),
                ('created_by', models.ForeignKey(limit_choices_to={'role': 'EVENT_MANAGER'}, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='main.userprofile')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('menus', models.ManyToManyField(related_name='tags', to='main.menu')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='main.restaurant')),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcements',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(limit_choices_to={'role': 'CUSTOMER'}, on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to='main.userprofile')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted_by', to='main.menu')),
            ],
            options={
                'verbose_name': 'Wishlist',
                'verbose_name_plural': 'Wishlists',
            },
        ),
    ]