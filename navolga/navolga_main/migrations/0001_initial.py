# Generated by Django 5.1.4 on 2025-01-12 07:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='The headline for the slide', max_length=200)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='slides/backgrounds/')),
                ('description', models.TextField(help_text='Detailed description or subtitle for the slide')),
                ('background_color', models.CharField(default='#FFFFFF', help_text='Background color in HEX (e.g., #FFFFFF for white)', max_length=7)),
                ('image', models.ImageField(help_text='Image displayed on the slide', upload_to='static/img/slides_images/')),
                ('alt_text', models.CharField(default='Slide image', help_text='Description of the image for accessibility', max_length=200)),
                ('app_store_url', models.URLField(blank=True, help_text='Link to the app on the App Store')),
                ('google_play_url', models.URLField(blank=True, help_text='Link to the app on Google Play')),
                ('is_active', models.BooleanField(default=True, help_text='Toggle to show or hide this slide')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='basket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategories', to='navolga_main.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_quantity', models.PositiveIntegerField()),
                ('dosage_form', models.CharField(blank=True, max_length=100, null=True)),
                ('strength', models.CharField(blank=True, max_length=50, null=True)),
                ('prescription_required', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('ingredient', models.CharField(blank=True, max_length=255, null=True)),
                ('age_suitable', models.CharField(blank=True, max_length=255, null=True)),
                ('size', models.CharField(blank=True, max_length=255, null=True)),
                ('side_effects', models.CharField(blank=True, max_length=255, null=True)),
                ('generic', models.CharField(blank=True, max_length=255, null=True)),
                ('works_by', models.CharField(blank=True, max_length=255, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/img/product_images/')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='navolga_main.category')),
            ],
        ),
    ]
