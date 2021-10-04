import uuid
import random
import string
from django.contrib import auth
import razorpay
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, response
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.mail import send_mail  
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from .models import Item, OrderItem, Order, Address, Payment, UserProfile, Wishlist,Contact
from .forms import UserForm, CheckoutForm, RefundForm,ContactForm


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'classyeveryday/login.html')
        else:
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                form = CheckoutForm()
                context = {
                    'form': form,
                    'object': order,
                }
                shipping_address_qs = Address.objects.filter(
                    user=self.request.user,
                    address_type='S',
                    default=True
                )
                if shipping_address_qs.exists():
                    context.update(
                        {'default_shipping_address': shipping_address_qs[0]})

                billing_address_qs = Address.objects.filter(
                    user=self.request.user,
                    address_type='B',
                    default=True
                )
                if billing_address_qs.exists():
                    context.update(
                        {'default_billing_address': billing_address_qs[0]})
                return render(self.request, "classyeveryday/checkout.html", context)
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("classyeveryday:home")

    def post(self,request, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the default shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('classyeveryday:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_customername=form.cleaned_data.get(
                        'shipping_customername')
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address1')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_landmark = form.cleaned_data.get(
                        'shipping_landmark')
                    shipping_city = form.cleaned_data.get(
                        'shipping_city')
                    shipping_state = form.cleaned_data.get(
                        'shipping_state')
                    shipping_zip = form.cleaned_data.get('shipping_zip')
                    shipping_phone = form.cleaned_data.get('shipping_phone')

                    if is_valid_form([shipping_customername,shipping_address1,shipping_city, shipping_state, shipping_zip]):
                            shipping_address = Address(
                            user=self.request.user,
                            customer_name=shipping_customername,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            landmark=shipping_landmark,
                            city=shipping_city,
                            state=shipping_state,
                            pincode=shipping_zip,
                            mobile=shipping_phone,
                            address_type='S'
                            )
                            print(shipping_address)
                            shipping_address.save()
                            order.shipping_address = shipping_address
                            order.save()

                            set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')

                            if set_default_shipping:
                                shipping_address.default = True
                                shipping_address.save()

                    else:
                        messages.error(
                            self.request, "Please fill in the required shipping address fields")
                        return redirect('classyeveryday:checkout')

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('classyeveryday:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_customername = form.cleaned_data.get(
                        'billing_customername')
                    billing_address1 = form.cleaned_data.get(
                        'billing_address1')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_landmark = form.cleaned_data.get(
                    'billing_landmark')
                    billing_city = form.cleaned_data.get(
                    'billing_city')
                    billing_state = form.cleaned_data.get(
                        'billing_state')
                    billing_zip = form.cleaned_data.get('billing_zip')
                    billing_mob = form.cleaned_data.get('billing_phone')

                    if is_valid_form([billing_customername,billing_address1,billing_city, billing_state, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            customer_name=billing_customername,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            landmark=billing_landmark,
                            city=billing_city,
                            state=billing_state,
                            pincode=billing_zip,
                            mobile=billing_mob,
                            address_type='B'
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.error(
                            self.request, "Please fill in the required billing address fields")
                        return redirect('classyeveryday:checkout')
                with transaction.atomic():
                    amount = int(order.get_total() * 100)
                    client = razorpay.Client(auth=('rzp_test_ZzejGouhiyW1FR','5H5ur62giVzTdF6K26XLXLYz'))
                    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
                    print(payment)
                    order.order_amount=order.get_total()
                    order.order_id=payment['id']
                    order.save()
                    billing_address.order_id=payment['id']
                    billing_address.save()
                    shipping_address.order_id=payment['id']
                    shipping_address.save()
                    return render(request,"classyeveryday/payment.html",{'payment':payment})
                
            else:
                print(form.errors)
                return redirect('classyeveryday:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("classyeveryday:order-summary")


class PaymentView(View):
    def post(self,request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        return render(request, 'classyeveryday/payment.html')

@csrf_exempt
def success(request):
    if request.method == 'GET':
        return render(request, 'classyeveryday/success.html')
    if request.method =='POST':
        a=request.POST
        order_id=""
        for key, val in a.items():
            if key== 'razorpay_order_id':
                order_id= val
                break

        order=Order.objects.get(user=request.user, ordered=False,order_id=order_id)

        # create the payment
        payment = Payment()
        payment.payment_id = order.order_id
        payment.user = request.user
        payment.amount = order.order_amount
        payment.save()

        order_items = order.items.all()
        order_items.update(ordered=True)
       
        for item in order_items:
            item.save()

        order.ordered = True
        order.payment = payment
        order.save()
        try: 
             send_mail_after_purchasing(order.user.email,order.user.username,order.order_id,order.order_amount,order_items)
        except Exception as e:
            print(e)
        newOrder=Order.objects.get(user=request.user,order_id=order_id,ordered=True)
        context={
            'neworder':newOrder
        }
        messages.success(request, "Your order has been Received")
        return render(request, 'classyeveryday/success.html',context)

def send_mail_after_purchasing(email,user,order_id,order_amount,order_items):
    subject="Your Order has been successfully Confirmed "
    message=f""" Dear {user}, Your Order has been successfully confirmed.
                Order Id: {order_id}
                Order Payment: {order_amount}
                order Items: {order_items}"""
    email_from=settings.EMAIL_HOST_USER
    receipent_list=[email]
    send_mail(subject,message,email_from,receipent_list)


class HomeView(ListView):
    model=Item
    template_name='classyeveryday/index.html'

    def get(self,request):
        newitem=Item.objects.filter(label='N')
        weekitem=Item.objects.filter(label='W')
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                print(order.order_amount)
                context = {
                    'newArrival': newitem,
                    'weekBest': weekitem,
                    'object': order
                }
                return render(request, 'classyeveryday/index.html', context)
            except ObjectDoesNotExist:
                context = {
                    'newArrival': newitem,
                    'weekBest': weekitem,
                }
                return render(request, 'classyeveryday/index.html', context)
        else:
            context = {
                'newArrival': newitem,
                'weekBest': weekitem,
            }
            return render(request, 'classyeveryday/index.html', context)

class ItemDetailView(DetailView):
    model=Item
    template_name='classyeveryday/product-layout-1.html'

    """def get(self,request):
        product = get_object_or_404(Item,)
        img=Images.objects.filter(image=product)
        context={
            'images':img
        }
        return render(request,'classyeveryday/product-layout-1.html',context)"""

def shop(request):
    if request.method=='GET':
        cat=request.GET.get('cat')
        sub=request.GET.get('sub')
        item=Item.objects.filter(category=cat,subcategory=sub)
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=request.user, ordered=False)
                context={
                    'items':item,
                    'object':order
                }
                return render(request,'classyeveryday/shop.html',context)
            except ObjectDoesNotExist:
                context = {
                    'items': item,
                }
                return render(request, 'classyeveryday/shop.html', context)
        else:
            context = {
                'items': item
            }
            return render(request, 'classyeveryday/shop.html', context)

def allprod(request):
    items=Item.objects.all()
    paginator = Paginator(items, 12) 
    page_number = request.GET.get('page')
    print(page_number)
    products_list = paginator.get_page(page_number)
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'items': products_list,
                'object': order
            }
            return render(request, 'classyeveryday/shop.html', context)
        except ObjectDoesNotExist:
            context = {
                'items': products_list,
            }
            return render(request, 'classyeveryday/shop.html', context)
    else:
        context = {
            'items': products_list
        }
        return render(request, 'classyeveryday/shop.html', context)


class OrderSummaryView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'classyeveryday/login.html')
        else:
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                context = {
                    'object': order
                }
                return render(self.request, 'classyeveryday/cart.html', context)
            except ObjectDoesNotExist:
                messages.warning(self.request, "You do not have an active order")
                return redirect("classyeveryday:home")

def order(request):
    if not request.user.is_authenticated:
        return render(request, 'classyeveryday/login.html')
    else:
        try:
            myorder = Order.objects.filter(user=request.user, ordered=True)
            #myOrder = Order.objects.get(user=request.user,ordered=True)
            context = {
                'object1':myorder,
            }
            return render(request,'classyeveryday/order.html',context)
        except ObjectDoesNotExist:
            return render(request, 'classyeveryday/order.html')

def about(request):
    return render(request,'classyeveryday/about.html')

def contact(request):
    if request.method=='GET':
        return render(request,'classyeveryday/contact-us.html')
    if request.method=='POST':
        form=ContactForm(request.POST or None)
        if form.is_valid():
            name=form.cleaned_data.get('name')
            email=form.cleaned_data.get('email')
            phone=form.cleaned_data.get('phone')
            subject=form.cleaned_data.get('subject')
            message=form.cleaned_data.get('message')
            if is_valid_form([name,email,message]):
                contactdata=Contact(
                    name=name,
                    email=email,
                    phone=phone,
                    subject=subject,
                    message=message
                )
                contactdata.save()
                messages.success(request,'We appreciate you contacting us. One of our colleagues will get back in touch with you soon!')
                return render(request,'classyeveryday/contact-us.html')
            else:
                messages.error(request,'Please fill all the required fields')
                return render(request,'classyeveryday/contact-us.html')


def wishlist(request):
    if not request.user.is_authenticated:
        return render(request, 'classyeveryday/login.html')
    else:
        wishlist = Wishlist.objects.filter(user=request.user)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'object': order,
                'wishlist':wishlist
            }
            return render(request,'classyeveryday/wishlist.html',context)
        except ObjectDoesNotExist:
            context={
                'wishlist': wishlist
            }
            return render(request, 'classyeveryday/wishlist.html', context)


def add_to_wishlist(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'classyeveryday/login.html')
    else:
        item = get_object_or_404(Item, slug=slug)
        data = Wishlist.objects.filter(user=request.user,items__slug=item.slug)
        if data.exists():
            messages.info(request, "This item is already in your wishlist.")
            return redirect("classyeveryday:wishlist")
        else:
            Wishlist.objects.create(user=request.user,items=item)
            messages.info(request, "This item was added to your Wishlist.")
            return redirect("classyeveryday:wishlist")


def remove_to_wishlist(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'classyeveryday/login.html')
    else:
        item = get_object_or_404(Item, slug=slug)
        Wishlist.objects.filter(user=request.user,items__slug=item.slug).delete()
        messages.info(request, "This item is remove from your wishlist.")
        return redirect("classyeveryday:wishlist")


def add_to_cart(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'classyeveryday/login.html')
    else:
        if request.method=='POST':
            item = get_object_or_404(Item, slug=slug)
            size = request.POST.get('option-1')
            qty = int(request.POST.get('quantity'))
            order_item, created = OrderItem.objects.get_or_create(
                item=item,
                user=request.user,
                size=size,
                quantity=qty,
                ordered=False
            )
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.items.filter(item__slug=item.slug ,size=size).exists():
                    order_item.quantity += qty
                    order_item.save()
                    messages.info(request, "This item quantity was updated.")
                    return redirect("classyeveryday:order-summary")
                else:
                    order.items.add(order_item)
                    messages.info(request, "This item was added to your cart.")
                    return redirect("classyeveryday:order-summary")
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(
                    user=request.user, ordered_date=ordered_date)
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return redirect("classyeveryday:order-summary")

def add_qty_to_cart(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'classyeveryday/login.html')
    else:
        if request.method=='GET':
            item = get_object_or_404(Item, slug=slug)
            order_item, created = OrderItem.objects.get_or_create(
                item=item,
                user=request.user,
                ordered=False
            )
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.items.filter(item__slug=item.slug).exists():
                    order_item.quantity += 1
                    order_item.save()
                    messages.info(request, "This item quantity was updated.")
                    return redirect("classyeveryday:order-summary")
                else:
                    order.items.add(order_item)
                    messages.info(request, "This item was added to your cart.")
                    return redirect("classyeveryday:order-summary")
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(
                    user=request.user, ordered_date=ordered_date)
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return redirect("classyeveryday:order-summary")



def remove_from_cart(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'classyeveryday/login.html')
    else:
        item = get_object_or_404(Item, slug=slug)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "This item was removed from your cart.")
                return redirect("classyeveryday:order-summary")
            else:
                messages.info(request, "This item was not in your cart")
                return redirect("classyeveryday:productDetail", slug=slug)
        else:
            messages.info(request, "You do not have an active order")
            return redirect("classyeveryday:productDetail", slug=slug)


def remove_single_item_from_cart(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'classyeveryday/login.html')
    else:
        item = get_object_or_404(Item, slug=slug)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order.items.remove(order_item)
                messages.info(request, "This item quantity was updated.")
                return redirect("classyeveryday:order-summary")
            else:
                messages.info(request, "This item was not in your cart")
                return redirect("classyeveryday:productDetail", slug=slug)
        else:
            messages.info(request, "You do not have an active order")
            return redirect("classyeveryday:productDetail", slug=slug)


#for REgister
class UserFormView(View):
    form_class = UserForm
    template_name = 'classyeveryday/register.html'

    # display Blank Form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Process from data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # Cleaned Data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email=form.cleaned_data['email']

            if User.objects.filter(email=email).first():
                messages.success(request,"Email is already taken")
                return redirect('/classyeveryday/register')
            user.set_password(password)
            user.save()
            auth_token=str(uuid.uuid4())
            profile_opj=UserProfile.objects.create(user=user,auth_token=auth_token)
            profile_opj.save()
            send_mail_after_registration(email,auth_token)
            return redirect("/classyeveryday/token/")

            # check the username and password in the database
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    newitem = Item.objects.filter(label='N')
                    weekitem = Item.objects.filter(label='W')
                    context = {
                        'newArrival': newitem,
                        'weekBest': weekitem
                    }
                    return render(request, 'classyeveryday/index.html',context)
        context = {
            "form": form
        }
        return render(request, 'classyeveryday/register.html', context)

def token(request):
    return render(request,'classyeveryday/token_send.html')

# send Mail
def send_mail_after_registration(email,token):
    subject="Your Account need to be verified"
    message=f'Click the link to verify your account http://localhost:8080/classyeveryday/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    receipent_list=[email]
    send_mail(subject,message,email_from,receipent_list)

def verify_user(request,auth_token):
    try:
        profile_obj=UserProfile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            UserProfile.is_verified=True
            UserProfile.save()
            messages.success(request,'Your Accounts Has been Verified ')
            return redirect("/classyeveryday/success_verified_user/")
        else:
            print("Error")

    except Exception as e:
        print(e)

def success_verified(request):
    return render(request,'classyeveryday/success_email.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            profile_obj=UserProfile.objects.filter(user=user).first()
            if not profile_obj.is_verified:
                messages.success(request,"Your account is not verified")
                return redirect('/classyeveryday/login_user')
            if user.is_active:
                login(request, user)
                newitem = Item.objects.filter(label='N')
                weekitem = Item.objects.filter(label='W')
                context = {
                    'newArrival': newitem,
                    'weekBest': weekitem
                }
                return render(request, 'classyeveryday/index.html',context)
            else:
                return render(request, 'classyeveryday/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'classyeveryday/login.html', {'error_message': 'Your username or password is incorrect'})
    return render(request, 'classyeveryday/login.html')

def forgot_psw(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        user=User.objects.filter(username=username).first()
        if not user:
            messages.info(request,'Username not found, Please Create your account')
            return redirect('/classyeveryday/register/')
        print(user.email)
        token=str(uuid.uuid4())
        profile_user=UserProfile.objects.filter(user=user).first()
        if profile_user:
            profile_user.auth_token=token
            profile_user.save()
        else:
            profile_obj=UserProfile.objects.create(user=user,auth_token=token)

        send_forget_password_mail(user.email,token)
        print(user.email)
        messages.success(request,'An email is sent, reset your password')
        return redirect('/classyeveryday/forgot_psw/')
    
    return render(request,'classyeveryday/forgot_psw.html')

def send_forget_password_mail(email,token):
    subject='Your Password reset link'
    message=f'Hi,click on the link to reset your password http://localhost:8080/classyeveryday/change_psw/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return True     


def change_psw(request,reset_psw_token):
    context={}
    try:
        profile_obj=UserProfile.objects.filter(auth_token=reset_psw_token).first()
        if not profile_obj:
            responseData = {
                        'Error':'link has been expired'
                    }
            return JsonResponse(responseData)

        context={'user_id' : profile_obj.user.id}
        if request.method=='POST':
            new_password=request.POST.get('psw')
            user_id=request.POST.get('user_id')
            user_obj=User.objects.filter(id=user_id).first()
            print(user_obj)
            if not user_obj:
                messages.info(request,'User not found')
                return redirect('/classyeveryday/login_user/')
            user_obj.set_password(new_password)
            user_obj.save()
            profile_user=UserProfile.objects.filter(user=user_obj).first()
            profile_user.auth_token=None
            profile_user.save()
            messages.info(request,'Password has been succesfully changed')
            return redirect('/classyeveryday/login_user')

    except Exception as e:
        print(e)
    
    return render(request,'classyeveryday/change_password.html',context)

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'classyeveryday/login.html', context)

def products(request):
    if request.method == 'GET':
        gender = request.GET.get('gen')
        item = Item.objects.filter(product_for=gender)
        paginator = Paginator(item, 12) 
        page_number = request.GET.get('page')
        products_list = paginator.get_page(page_number)
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=request.user, ordered=False)
                context = {
                    'items': products_list,
                    'object': order
                }
                return render(request, 'classyeveryday/shop.html', context)
            except ObjectDoesNotExist:
                context = {
                    'items': products_list,
                }
                return render(request, 'classyeveryday/shop.html', context)
        else:
            context = {
                'items': products_list
            }
            return render(request, 'classyeveryday/shop.html', context)

def catprod(request):
    if request.method == 'GET':
        cat = request.GET.get('cat')
        item = Item.objects.filter(category=cat)
        paginator = Paginator(item, 12) 
        page_number = request.GET.get('page')
        products_list = paginator.get_page(page_number)
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=request.user, ordered=False)
                context = {
                    'items': products_list,
                    'object': order
                }
                return render(request, 'classyeveryday/shop.html', context)
            except ObjectDoesNotExist:
                context = {
                    'items': products_list,
                }
                return render(request, 'classyeveryday/shop.html', context)
        else:
            context = {
                'items': products_list
            }
            return render(request, 'classyeveryday/shop.html', context)

def privacy(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'object': order
            }
            return render(request, 'classyeveryday/privacy.html', context)
        except ObjectDoesNotExist:
            return render(request, 'classyeveryday/privacy.html')
    else:
        return render(request, 'classyeveryday/privacy.html')

def tnc(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'object': order
            }
            return render(request, 'classyeveryday/tnc.html', context)
        except ObjectDoesNotExist:
            return render(request, 'classyeveryday/tnc.html')
    else:
        return render(request, 'classyeveryday/tnc.html')

def refund(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'object': order
            }
            return render(request, 'classyeveryday/refund.html', context)
        except ObjectDoesNotExist:
            return render(request, 'classyeveryday/refund.html')
    else:
        return render(request, 'classyeveryday/refund.html')

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(category__icontains=query) | Q(slug__icontains=query)

            results = Item.objects.filter(lookups).distinct()
            context = {'results': results,
                       'submitbutton': submitbutton}

            return render(request, 'classyeveryday/search.html', context)
        else:
            return render(request, 'classyeveryday/search.html')
    else:
        return render(request,'classyeveryday/search.html')