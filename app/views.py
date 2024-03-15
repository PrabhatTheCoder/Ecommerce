from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import RegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

def home(request):
 return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request,'app/home.html',{'topwears':topwears, 'bottomwears': bottomwears,'mobiles' :mobiles})

class product_detailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product':product})

class CustomerRegistration(View):
    def get(self, request):
        forms = RegistrationForm()
        
        return render(request,'app/customerregistration.html', {'forms':forms})

    def post(self, request):
        forms = RegistrationForm(request.POST)
        print(forms)
        if forms.is_valid():
            forms.save()
            messages.success(request, 'Congratulations!! Registered Successfully')
        return render(request,'app/customerregistration.html', {'forms':forms})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    reg = Cart(user = user, product = product)
    reg.save()
    return HttpResponseRedirect('/cart/')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        
        for p in cart_product:
            temp_amt = (p.quantity * p.product.selling_price)
            amount += temp_amt
            print(amount)
        total_amount = amount + shipping_amount
        print("total_amt",total_amount)
        
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' :total_amount
        }
        
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        
        for p in cart_product:
            temp_amt = (p.quantity * p.product.selling_price)
            amount += temp_amt
            print(amount)
        total_amount = amount + shipping_amount
        print("total_amt",total_amount)
        
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' :total_amount
        }
        
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        
        for p in cart_product:
            temp_amt = (p.quantity * p.product.selling_price)
            amount += temp_amt
            print(amount)
        total_amount = amount + shipping_amount
        print("total_amt",total_amount)
        
        data = {
            'amount' : amount,
            'totalamount' :total_amount
        }
        
        return JsonResponse(data)
        
        

def ShowCart(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user = user)
        print(carts)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        
        if cart_product:
            for p in cart_product:
                temp_amt = (p.quantity * p.product.selling_price)
                amount += temp_amt
                print(amount)
            total_amount = amount + shipping_amount
            print("total_amt",total_amount)
            return render(request, 'app/show_cart.html',{'carts':carts, 'total_amt':total_amount, 'amount':amount})
        return render(request,'app/emptycart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

class ProfileView(View):
    def get(self,request):
        forms = CustomerProfileForm()
        return render(request, 'app/profile.html',{'forms':forms, 'active':'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        print(form)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']

            reg = Customer(user=usr,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
        return HttpResponseRedirect('/profile')

def address(request):
    address = Customer.objects.filter(user = request.user)
    print(address)
    return render(request, 'app/address.html',{'address':address, 'active':'btn-primary'})

def orders(request):
    op = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category = 'M')
    elif data == 'samsung' or data == 'iphone':
        mobiles = Product.objects.filter(category = 'M').filter(brand = data)
    elif data == 'below':
        mobiles = Product.objects.filter(category = 'M').filter(selling_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category = 'M').filter(selling_price__gt=10000)
    return render(request, 'app/mobile.html',{'mobiles' : mobiles})

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    print(cart_product)
    
    if cart_product:
        for p in cart_product:
            temp_amt = (p.quantity * p.product.selling_price)
            amount += temp_amt
            print(amount)
        total_amount = amount + shipping_amount
        print("total_amt",total_amount)
    
    return render(request, 'app/checkout.html',{'add':add, 'total_amt':total_amount, 'cart_items':cart_items})

def payment_done(request):
    cust_id = request.GET.get("custid")
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")