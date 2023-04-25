from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm 
from .models import Product,Order, Payment
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from .forms import RegForm, FeedbackForm, PaymentForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View
from .filters import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
# Create your views here.

from django.shortcuts import render, redirect
from .models import Product,Category
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

def home(request):
    product = Product.objects.all()
    fast = Product.objects.filter(choice_id=1)
    local = Product.objects.filter(choice_id=2)
    beef  =  Product.objects.filter(choice_id = 3 )
    drink  =  Product.objects.filter(choice_id = 4 )
    feed = Feedback.objects.all().order_by("?")
    context = {'product':product,'fast':fast,'local':local,'beef':beef,'drink':drink,'feed':feed}
    return render(request, 'index.html',context)


def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    kent = product.slug
    cart.add(product=product)
    print(cart)
    return HttpResponseRedirect(reverse("details",args={product.slug}))



def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart-detail")


# @login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart-detail")


# @login_required(login_url="/users/login")
def item_decrement(request, id):
    try:
        cart = Cart(request)
        product = Product.objects.get(id=id)
        cart.decrement(product=product)
        return redirect("cart-detail")
    except:
        messages.error(request,"not possible agba hacker")
        return redirect("cart-detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart-detail")


# @login_required(login_url="login")
def cart_detail(request):
    # if request.user.is_authenticated:
    sum = 0.0
    cart = Cart(request)
    for key,value in request.session.get('cart').items():
        # print("this is price",value['price'])
        c = float(value['price'])*float(value['quantity'])
        print("this is combined ",c)
        sum+=c
        print("this is total sum",sum)
    form = PaymentForm(request.POST)

    if form.is_valid():
        payment = form.save()
        
        
        return render(request, 'make-pay.html', {'payment':payment,'amount_value': payment.amount_value()})
        
    
    else:
        
        form = PaymentForm(initial = {'username':request.user,'email':request.user.email,'amount':sum})
        return render(request,'cart.html',{'form':form,'sum':sum})
        # html = render_to_string('cart.html', {'cart': cart,'form':form,'sum':sum})
        # data = {'html': html, 'total': cart.get_total_price()}
        # return JsonResponse(data)
   



def register(request):
 
    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
        form = RegForm(request.POST)
 
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            if User.objects.filter(email=email):
                messages.error(request, 'email already taken ')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'username already taken ')
                return redirect('register')
            else:
                user = authenticate(username = username,password = password)
                auth.login(request, user)
                return redirect('home')
         
        else:
            return render(request,'signin.html',{'form':form})
     
    else:
        form = RegForm()
        return render(request,'signin.html',{'form':form})


def login(request):

    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'invalid login details')
            form = AuthenticationForm()
            return render(request,'login.html',{'form':form})
     
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
    
    
 
def logout(request):
    request.session.clear()
    return redirect('login')

def details(request, slug):
    try:
        cart = request.session.get('cart', {})

# Get the number of items in the cart
        num_items = len(cart)
        product = Product.objects.get(slug=slug)
        feedback = Feedback.objects.filter(product_id=product)
        count =  feedback.count()
        if request.method == 'POST':
            
            form = FeedbackForm(request.POST)
        
            if form.is_valid():
                username = form.cleaned_data['username']
                if feedback.filter(username=username).exists():
                    messages.error(request,'you can only send one feedback per product')
                    return HttpResponseRedirect(reverse("details",args={product.slug}))
                else:
                    form.save()
                    return HttpResponseRedirect(reverse("details",args={product.slug}))
            else:
                messages.error(request, 'something no clear ')
                form = FeedbackForm(initial = {'username':request.user.id,'product':product})
                return render(request, 'detail.html', {'product': product,'form':form,'feedback':feedback,'count':count,'num_items':num_items})
        else:
            form = FeedbackForm(initial = {'username':request.user.id,'product':product})
        return render(request, 'detail.html', {'product': product,'form':form,'feedback':feedback,'count':count,'num_items':num_items})
    except:
        messages.error(request,'register to have full access ')
        return redirect('register')



# class CheckOut(View):
def checkout(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            customer = request.session.get(User)
            cart = Cart(request)
            proof = request.FILES.get('proof')
            # product = Product.objects.get(id=request.session.get('cart').items[1])
            # print(int(product.product_id))
            for key,value in request.session.get('cart').items():
            

            # for product in product:
                products = Product.objects.filter(id=value['product_id'])
                for i in products:
                    order = Order(customer=User(id=request.user.id),
                                    product=i,
                                    price=float(value['price']),
                                    address=address,
                                    image = proof,
                                    phone=phone,
                                    quantity=value['quantity'])
                    order.save()
            request.session['cart'] = {}

        return redirect('cart-detail')
    else:
        messages.error(request,'you much login to checkout')
        return redirect('login')

def order(request):
    if request.user.is_authenticated:
        
        orders = Order.objects.filter(customer_id=request.user.id)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})
    else:
        messages.error(request,'its not possible agba')
        return redirect('home')
    
def restaurants(request):
    search = request.GET.get('search')
    if request.method =="GET":
        if search:
            category= Category.objects.filter(choice__icontains=search)
            return render(request,'restaurants.html',{'category':category})
        else:
            category = Category.objects.all()
            
            
    return render(request,'restaurants.html',{'category':category})

def restaurant_details(request,slug):
    category = Category.objects.get(slug=slug)
    product = Product.objects.filter(choice_id=category)
    
    return render(request,'restaurant-details.html',{'category':category,'product':product})
def delete(request, product_id):
    c = request.session.get('cart',[product_id]==product_id)
    c.pop(product_id)
    request.session.modified = True

    return redirect('cart-detail')


def payment(request):
    if request.user.is_authenticated:
        sum = 0.0
        cart = Cart(request)
        for key,value in request.session.get('cart').items():
            # print("this is price",value['price'])
            c = float(value['price'])*float(value['quantity'])
            print("this is combined ",c)
            sum+=c
            print("this is total sum",sum)
    
    
        pk = settings.PAYSTACK_PUBLIC_KEY
        if request.method == 'POST':

            form = PaymentForm(request.POST)
    
            if form.is_valid():
                payment = form.save()
             
                
                return render(request, 'make-pay.html', {'payment':payment,'amount_value': payment.amount_value()})
                
            
            else:
                return render(request,'payment.html',{'form':form,'sum':sum})
            
        
        else:
            form = PaymentForm(initial = {'username':request.user,'email':request.user.email,'amount':sum})
            return render(request,'payment.html',{'form':form,'sum':sum})
    else:
        return redirect('login')
    
def verify(request, ref:str):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()

    if verified:
        messages.success(request, f'{payment.amount} paid sucessfully')
        customer = request.session.get(User)
        cart = Cart(request)
        proof = request.FILES.get('proof')
        # product = Product.objects.get(id=request.session.get('cart').items[1])
        # print(int(product.product_id))
        for key,value in request.session.get('cart').items():
        

        # for product in product:
            products = Product.objects.filter(id=value['product_id'])
            for i in products:
                order = Order.objects.create(customer=User(id=request.user.id),
                                product=i,
                                price=float(value['price']),
                                address=payment.address,
                                image = proof,
                                phone=payment.phone,
                                status = True,
                                quantity=value['quantity']),
                                
                # order.save()
        request.session['cart'] = {}
        return render(request, "success.html")
    else:
        messages.success(request, f'{payment.amount} wasnt sucessfully')
    
    return redirect('payment')
