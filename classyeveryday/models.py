from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.contrib.auth.models import Permission, User


CATEGORY_CHOICES=(
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
    ('W','Watches'),
    ('F','Footwear'),
    ('WW','Winter Wear'),
    ('EW','Ethnic Wear'),
    ('WM','Women Western & Maternity Wear'),
    ('LS','Lingerie & Sleepwear'),
    ('A','Accessories'),
    ('M','Mobile'),
    ('MA','Mobile Accessories')
)
SUBCATEGORY_CHOICES=(
    ('T','T-Shirts'),
    ('CS','Casual Shirts'),
    ('FS','Formal Shirts'),
    ('J','Jeans'),
    ('CT','Casual Trousers'),
    ('FT','Formal Trousers'),
    ('FT','Formal Trousers'),
    ('TP','Track Pants'),
    ('S','Shorts'),
    ('C','Cargos'),
    ('SS','Sweatshirts'),
    ('J','Jackets'),
    ('S','Sweater'),
    ('TS','Tracksuits'),
    ('K','Kurta'),
    ('ES','Ethnic Sets'),
    ('SH','Sherwani'),
    ('P','Pyjama'),
    ('D','Dhoti'),
    ('L','Lungi'),
    ('SS','Sport Shoes'),
    ('CAS','Casual Shoes'),
    ('FOS','Formal Shoes'),
    ('SN','Sandals'),
    ('FF','Flip Flopes'),
    ('BO','Boots'),
    ('LO','Loafers'),
    ('RUS','Running Shoes'),
    ('SNE','Sneakers'),
    ('B','Backpacks'),
    ('FT','Fastrack'),
    ('CA','Casio'),
    ('TI','Titan'),
    ('FO','Fossil'),
    ('SON','Sonata'),
    ('WL','Wallets'),
    ('BL','Belts'),
    ('SUN','Sunglasses'),
    ('LT','Luggage and Travel'),
    ('FR','Frames'),
    ('JW','Jewellery'),
    ('HD','Handbags'),
    ('SB','Shoulder Bags'),
    ('TOT','Totes'),
    ('SLB','Slings Bags'),
    ('CL','Clutches'),
    ('FLA','Flat'),
    ('HE','Heels'),
    ('WD','Wedges'),
    ('TWW','Topwear of women'),
    ('DR','Dresses'),
    ('SH','Shorts'),
    ('SK','Skirts'),
    ('JT','Jeggings and Tights'),
    ('TCW','Trousers and Capris of women'),
    ('BRA','Bras'),
    ('PN','Panties'),
    ('ND','Night Dresses and Nighties'),
    ('LS','Lingerie Sets'),
    ('SW','Shapewear'),
    ('CMS','Camisoles & Slips'),
    ('SAR','Sarees'),
    ('KK','Kurtas & Kurtis'),
    ('DM','Dress Material'),
    ('LC','Lehenga Choli'),
    ('BL','Blouse'),
    ('SWS','Salwar Suits'),
    ('GOW','Gowns'),
    ('DUP','Dupattas'),
    ('PAL','Palazzos'),
    ('SRA','Shararas'),
    ('DP','Dhoti Pants'),
    ('ETT','Ethnic Trousers'),
    ('PET','Petticoats'),
    ('MI','Mi'),
    ('RM','Realme'),
    ('APP','Apple'),
    ('VI','Vivo'),
    ('OPP','Oppo'),
    ('ASU','Asus'),
    ('SAM','Samsung'),
    ('HN','Honor'),
    ('INF','Infinix'),
    ('PX','POCO X2'),
    ('RMN','Realme Nazro 10'),
    ('MC','Mobile Cases'),
    ('HH','Headphones & Headsets'),
    ('PB','Power Banks'),
    ('SG','Screenguards'),
    ('MMC','Memory Cards'),
    ('SHH','Smart Headphones'),
    ('MCA','Mobile Cabels'),
    ('MCG','Mobile Charges'),
    ('MH','Mobile Holders'),
)

GENDER_CHOICES=(
    ('M','Men'),
    ('W','Women')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

LABEL_CHOICES = (
    ('N','New Arrival'),
    ('W','Weekly Bestseller')
)

CHOOSE_SIZES=(
    ('XS','Xtra Small'),
    ('S','Small'),
    ('M','Medium'),
    ('L','Large'),
    ('XL','Xtra Large'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9')
)

STOCK=(
    ('IN','IN'),
    ('OUT','OUT')
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=200,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.user.username

class Item(models.Model):
    title=models.CharField(max_length=50)
    price=models.FloatField()
    discount_price=models.FloatField()
    category=models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    subcategory=models.CharField(choices=SUBCATEGORY_CHOICES,max_length=3)
    label=models.CharField(choices=LABEL_CHOICES, max_length=1,default='N')
    slug=models.SlugField()
    stock=models.CharField(choices=STOCK,max_length=10,default='IN')
    #image = models.ForeignKey(Images,on_delete=models.CASCADE,blank=True ,null=True)
    productimage=models.FileField()
    description=models.TextField()
    product_for=models.CharField(choices=GENDER_CHOICES, max_length=2,blank=True ,null=True)
    
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("classyeveryday:productDetail", kwargs={
            'slug':self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("classyeveryday:add-to-cart", kwargs={
            'slug':self.slug
        })

    def get_add_qty_to_cart_url(self):
        return reverse("classyeveryday:add-qty-to-cart", kwargs={
            'slug': self.slug
        })
    def get_add_to_wishlist_url(self):
        return reverse("classyeveryday:add-to-wishlist", kwargs={
            'slug':self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("classyeveryday:remove-from-cart", kwargs={
            'slug':self.slug
        })

    def get_remove_from_wishlist_url(self):
        return reverse("classyeveryday:remove-to-wishlist", kwargs={
            'slug': self.slug
        })

#For variation
class Variation (models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    size = models.CharField(max_length=120, choices=CHOOSE_SIZES)

    def __str__(self):
        return f"{self.item.title} of {self.item.slug}"

class Multipleimages (models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    images = models.FileField()

    def __str__(self):
        return f"{self.item.title} of {self.item.slug}"

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item= models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered= models.BooleanField(default=False)
    quantity=models.IntegerField()
    size=models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.title} of {self.item.slug}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items= models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.items.title

    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    order_id = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date= models.DateTimeField()
    order_amount=models.FloatField( blank=True, null=True)
    ordered= models.BooleanField(default=False)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code
    
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    customer_name=models.CharField(max_length=50)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode= models.CharField(max_length=10)
    mobile=models.IntegerField()
    order_id=models.CharField(max_length=20)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Payment(models.Model):
    payment_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

  
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    phone=models.IntegerField()
    subject=models.CharField(max_length=50)
    message=models.TextField(max_length=500)

    def __str__(self):
        return self.name



"""def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)"""
