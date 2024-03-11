from django.shortcuts import render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import RegistrationForm
from django.contrib import messages

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
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

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
 return render(request, 'app/checkout.html')
