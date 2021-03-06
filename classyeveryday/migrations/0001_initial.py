# Generated by Django 3.1.3 on 2020-11-10 08:32

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
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=50)),
                ('street_address', models.CharField(max_length=100)),
                ('apartment_address', models.CharField(max_length=100)),
                ('landmark', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('mobile', models.IntegerField()),
                ('address_type', models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping')], max_length=1)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('discount_price', models.FloatField()),
                ('category', models.CharField(choices=[('TW', 'Top Wear'), ('BW', 'Bottom Wear'), ('W', 'Watches'), ('F', 'Footwear'), ('WW', 'Winter Wear'), ('EW', 'Ethnic Wear'), ('WM', 'Women Western & Maternity Wear'), ('LS', 'Lingerie & Sleepwear'), ('A', 'Accessories'), ('M', 'Mobile'), ('MA', 'Mobile Accessories')], max_length=3)),
                ('subcategory', models.CharField(choices=[('T', 'T-Shirts'), ('CS', 'Casual Shirts'), ('FS', 'Formal Shirts'), ('J', 'Jeans'), ('CT', 'Casual Trousers'), ('FT', 'Formal Trousers'), ('FT', 'Formal Trousers'), ('TP', 'Track Pants'), ('S', 'Shorts'), ('C', 'Cargos'), ('SS', 'Sweatshirts'), ('J', 'Jackets'), ('S', 'Sweater'), ('TS', 'Tracksuits'), ('K', 'Kurta'), ('ES', 'Ethnic Sets'), ('SH', 'Sherwani'), ('P', 'Pyjama'), ('D', 'Dhoti'), ('L', 'Lungi'), ('SS', 'Sport Shoes'), ('CAS', 'Casual Shoes'), ('FOS', 'Formal Shoes'), ('SN', 'Sandals'), ('FF', 'Flip Flopes'), ('BO', 'Boots'), ('LO', 'Loafers'), ('RUS', 'Running Shoes'), ('SNE', 'Sneakers'), ('B', 'Backpacks'), ('FT', 'Fastrack'), ('CA', 'Casio'), ('TI', 'Titan'), ('FO', 'Fossil'), ('SON', 'Sonata'), ('WL', 'Wallets'), ('BL', 'Belts'), ('SUN', 'Sunglasses'), ('LT', 'Luggage and Travel'), ('FR', 'Frames'), ('JW', 'Jewellery'), ('HD', 'Handbags'), ('SB', 'Shoulder Bags'), ('TOT', 'Totes'), ('SLB', 'Slings Bags'), ('CL', 'Clutches'), ('FLA', 'Flat'), ('HE', 'Heels'), ('WD', 'Wedges'), ('TWW', 'Topwear of women'), ('DR', 'Dresses'), ('SH', 'Shorts'), ('SK', 'Skirts'), ('JT', 'Jeggings and Tights'), ('TCW', 'Trousers and Capris of women'), ('BRA', 'Bras'), ('PN', 'Panties'), ('ND', 'Night Dresses and Nighties'), ('LS', 'Lingerie Sets'), ('SW', 'Shapewear'), ('CMS', 'Camisoles & Slips'), ('SAR', 'Sarees'), ('KK', 'Kurtas & Kurtis'), ('DM', 'Dress Material'), ('LC', 'Lehenga Choli'), ('BL', 'Blouse'), ('SWS', 'Salwar Suits'), ('GOW', 'Gowns'), ('DUP', 'Dupattas'), ('PAL', 'Palazzos'), ('SRA', 'Shararas'), ('DP', 'Dhoti Pants'), ('ETT', 'Ethnic Trousers'), ('PET', 'Petticoats'), ('MI', 'Mi'), ('RM', 'Realme'), ('APP', 'Apple'), ('VI', 'Vivo'), ('OPP', 'Oppo'), ('ASU', 'Asus'), ('SAM', 'Samsung'), ('HN', 'Honor'), ('INF', 'Infinix'), ('PX', 'POCO X2'), ('RMN', 'Realme Nazro 10'), ('MC', 'Mobile Cases'), ('HH', 'Headphones & Headsets'), ('PB', 'Power Banks'), ('SG', 'Screenguards'), ('MMC', 'Memory Cards'), ('SHH', 'Smart Headphones'), ('MCA', 'Mobile Cabels'), ('MCG', 'Mobile Charges'), ('MH', 'Mobile Holders')], max_length=3)),
                ('label', models.CharField(choices=[('N', 'New Arrival'), ('W', 'Weekly Bestseller')], default='N', max_length=1)),
                ('slug', models.SlugField()),
                ('available_size', models.CharField(blank=True, max_length=100, null=True)),
                ('productimage', models.FileField(upload_to='')),
                ('description', models.TextField()),
                ('product_for', models.CharField(blank=True, choices=[('M', 'Men'), ('W', 'Women')], max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.CharField(blank=True, max_length=20, null=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('being_delivered', models.BooleanField(default=False)),
                ('received', models.BooleanField(default=False)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='classyeveryday.address')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classyeveryday.coupon')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classyeveryday.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(blank=True, max_length=50, null=True)),
                ('one_click_purchasing', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classyeveryday.order')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('size', models.CharField(blank=True, max_length=5, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classyeveryday.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='classyeveryday.OrderItem'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classyeveryday.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='classyeveryday.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
