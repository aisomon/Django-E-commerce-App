from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from product.models import Product, Comment,ProductCategories
from order.models import ShopCart
from .models import Setting,ContactMessage,FAQ
from django.contrib import messages
from user.models import UserProfile
from order.models import Order, OrderProduct

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.crypto import get_random_string

# Create your views here.


def home(request):
    product_slider = Product.objects.all().order_by('id')[:4]
    product_latest = Product.objects.all().order_by('-id')[:4] #last 4 products
    product_picked = Product.objects.all().order_by('?')[:4] #random selected product

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity

    page="index"
    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        'product_slider':product_slider,
        'product_latest':product_latest,
        'product_picked':product_picked,
        'page':page,
        "shopcart" : shopcart,
        "total" : total,
        "q" : q,
    }

    return render(request, 'index.html',context=context)

def product_detail(request,id):
    signle_product = Product.objects.filter(pk=id)
    product_picked = Product.objects.all().order_by('?')[:4] #random selected produc
    comments = Comment.objects.filter(product_id=id,status=True)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity
    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        'signle_product':signle_product,
        'product_picked':product_picked,
        'comments':comments,
        'total':total,
        'q':q,
        
    }
    return render(request, 'product.html',context=context)

@login_required(login_url='/login')
def addcomment(request,id):
    url = request.META.get('HTTP_REFERER') #get last url
    if request.method == 'POST':
        data = Comment()  # create relation with model
        data.subject = request.POST.get('subject')
        data.comment = request.POST.get('comment')
        data.rate = request.POST.get('rate')
        data.ip = request.META.get('REMOTE_ADDR')
        data.product_id=id
        current_user= request.user
        data.user_id=current_user.id
        data.save()  # save data to table
        messages.success(request, "Your review has ben sent. Thank you for your interest.")
        return HttpResponseRedirect(url)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        }

    return render(request, 'login.html',context)

def signup(request):    
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user( first_name=first_name, last_name=last_name,username=username,email=email,password=password)
        user.save()
        created_user = authenticate(username=username, password=password)
        login(request, created_user)
        #Create data in profile table for user
        current_user = request.user
        data = UserProfile()
        data.user_id = current_user.id
        data.name = last_name
        data.image="images/users/user.png"
        data.save()

        messages.success(request, 'Your account has been created!')
        return HttpResponseRedirect('/')
    
    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
    }
    return render(request, 'user_create.html',context=context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def cart(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        q += rs.quantity
    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        "shopcart" : shopcart,
        "total" : total,
        "q":q,
    }
    return render(request, 'cart.html', context=context)

@login_required(login_url='/login')
def checkout(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity
    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    data = Order()
    if request.method == "POST":
        data.full_name = request.POST.get("name")
        data.address = request.POST.get("address")
        data.city = request.POST.get("city")
        data.country = request.POST.get("country")
        data.phone = request.POST.get("tel")
        data.user_id = current_user.id
        data.ip = request.META.get('REMOTE_ADDR')
        data.total = total
        orderCode = get_random_string(5).upper()
        data.code = orderCode
        data.save()

        for rs in shopcart:
            detail = OrderProduct()
            detail.order_id = data.id
            detail.product_id = rs.product_id
            detail.user_id = current_user.id
            detail.quantity = rs.quantity
            detail.price = rs.product.price
            detail.amount = total
            detail.save()
        ShopCart.objects.filter(user_id=current_user.id).delete()#clear and delete shopcart
        messages.success(request,"Your order has been completed. Thank you.")
        return render(request, 'order_Completed.html',{'orderCode':orderCode,'category':catagories})
    context = {
        "catagories":catagories,
        "setting":setting,
        'total':total,
        'q':q,
    }
    return render(request, 'checkout.html',context=context)

def aboutus(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity

    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        'total':total,
        'q':q,
    }
    return render(request, 'about.html',context=context)

def contact(request):
    if request.method == 'POST':
        full_name = request.POST.get("fullName")
        email = request.POST.get("email")
        message = request.POST.get("message")
        data = ContactMessage(name=full_name,email=email,message=message)
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        return JsonResponse({
            "msg":"Success"  
        })
    if request.method == 'GET':
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id = current_user.id)
        total = 0
        q = 0
        for s in shopcart:
            total += s.product.price * s.quantity
            q += s.quantity
        setting = Setting.objects.all()
        catagories = ProductCategories.objects.all()
        context = {
            "catagories":catagories,
            "setting":setting,
            'total':total,
            'q':q,
        }
        return render(request, 'contact.html',context=context)

@login_required(login_url='/login')
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER') #get last url
    current_user = request.user
    product= Product.objects.get(pk=id)

    checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
    if checkinproduct:
        control = 1 # The product is in the cart
    else:
        control = 0 # The product is not in the cart"""
    if request.method == "POST":
        if control == 1:
            data = ShopCart.objects.get(product_id=id,user_id=current_user.id)
            data.quantity += int(request.POST.get("quantity"))
            data.save()

        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = request.POST.get("quantity")
            data.save()
        messages.success(request, "Product added to shopcart ")
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id,user_id=current_user.id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to shopcart")
        return HttpResponseRedirect(url)

    return render(request, 'index.html')

@login_required(login_url='/login')
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Deleted succesfully !")
    return HttpResponseRedirect("/cart")


def viewall(request):
    data = Product.objects.all()
    search = request.GET.get('q')
    if search:
        data=data.filter(
            Q(title__icontains = search)|Q(description__icontains = search)|Q(price__icontains = search)
        )
    paginator = Paginator(data,8)# Show 8 products per page.
    page_number = request.GET.get('page')
    all_data = paginator.get_page(page_number)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity
    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        'total':total,
        'q':q,
        "data":data,
        'all_data': all_data,
    }
    return render(request,'products.html',context=context)

def women(request):
    product_categories = ProductCategories.objects.get(user_type="Women")
    data = Product.objects.filter(categorie_id = product_categories.id)
    search = request.GET.get('q')
    if search:
        data=data.filter(
            Q(title__icontains = search)|Q(description__icontains = search)|Q(price__icontains = search)
        )
    paginator = Paginator(data,8)# Show 8 products per page.
    page_number = request.GET.get('page')
    all_data = paginator.get_page(page_number)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity
    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        'total':total,
        'q':q,
        "data":data,
        'all_data': all_data,
    }
    return render(request,'products.html',context=context)

def men(request):
    product_categories = ProductCategories.objects.get(user_type="Men")
    data = Product.objects.filter(categorie_id = product_categories.id)
    search = request.GET.get('q')
    if search:
        data=data.filter(
            Q(title__icontains = search)|Q(description__icontains = search)|Q(price__icontains = search)
        )
    paginator = Paginator(data,8)# Show 8 products per page.
    page_number = request.GET.get('page')
    all_data = paginator.get_page(page_number)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity
    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        'total':total,
        'q':q,
        "data":data,
        'all_data': all_data,
    }
    return render(request,'products.html',context=context)

@login_required(login_url='/login')
def user_profile(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user)
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity

    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        'total':total,
        'q':q,
        'profile':profile,
    }
    return render(request, 'user_profile.html',context=context)

@login_required(login_url='/login')
def user_update(request):
    current_user = request.user
    if request.method == "POST":
        user = current_user
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        image = request.FILES.get("photo")
        UserProfile.objects.filter(user_id = user.id).update(name=name,phone=phone,address=address,city=city,country=country)
        ob = UserProfile.objects.get(user_id=user.id)
        ob.image = image
        ob.save()
        messages.success(request,"Your profile is updated successfully!")
    profile = UserProfile.objects.get(user_id=current_user)
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity

    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        'total':total,
        'q':q,
        'profile':profile,
    }
    return render(request, 'user_update.html',context=context)

@login_required(login_url='/login')
def user_orders(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user)
    orders = Order.objects.filter(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity

    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    context = {
        "catagories":catagories,
        "setting":setting,
        'total':total,
        'q':q,
        'profile':profile,
        'orders': orders,
    }
    return render(request,"user_orders.html",context=context)


def faq(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    q = 0
    for s in shopcart:
        total += s.product.price * s.quantity
        q += s.quantity
    setting = Setting.objects.all()
    catagories = ProductCategories.objects.all()
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    context = {
        "catagories":catagories,
        "setting":setting,
        'total':total,
        'q':q,
        'faq': faq,
    }
    return render(request,"faq.html",context=context)