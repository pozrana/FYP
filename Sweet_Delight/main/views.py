from datetime import date
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from . models import FoodMenu, ImageGallery
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def index(request):
    menus = FoodMenu.objects.all()
    galleries = ImageGallery.objects.all()

    return render(request, 'index.html', {'menus': menus, 'galleries': galleries})

    


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pw1 = request.POST['pw1']
        pw2 = request.POST['pw2']

        if pw1 == pw2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken.')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken.')
            else:
                user = User.objects.create_user(username=username, password=pw1, first_name=fname, last_name=lname, email=email,)
                user.save()
                messages.info(request,'The user has been registered.')
                return redirect('/login/')
        else:
            messages.info(request, 'Password not matching.')
        
        return redirect ('/register/')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        pw1 = request.POST['pw1']

        user = auth.authenticate(username=username, password=pw1)

        if user is not None:
            auth.login(request, user)
            return redirect('/dashboard/')
        else:
            messages.info(request,'Invalid username or password.')
            return redirect('/login/')
    else: 
        return render(request, 'login.html')
        
def logout(request):
    auth.logout(request)
    return redirect('login/')
       

    #     appuser = User.objects.create_user(username, email, pw1, pw2)
    #     appuser.first_name = fname
    #     appuser.last_name = lname
        
    #     appuser.save()
    #     messages.success(request,"Your Account has been successfully created")

    #     return redirect('login')

    # if request.method == "POST":
    #     username = request.POST['username']
    #     pw1 = request.POST['pw1']    

    #     User = authenticate(username=username, password=pw1)

    #     if user is not None:
    #         signup(request, user)
    #         fname = user.first_name
    #         return render(request, "authentication/index.html", {'fname': fname})
    #     else:
    #         messages.error(request, "Login Error!")
    #         return redirect('index')
    
    
    return render(request, 'login.html')

def booking(request):
    # if request.method == "POST":
        
        # month = request.POST['month']
        # date = request.POST['date']
        # hours = request.POST['hours']
        # event = request.POST['event']
        # fullname = request.POST['fullname']
        # mobile = request.POST['mobile']
        # people = request.POST['people']
        
        return render(request, 'booking.html')
    # else: 
    #     return render(request, 'home.html')

def cart(request):
    return render(request, 'cart.html')   

# def contact(request):
#     if request.method == "POST":
#         contact_name = request.POST['contact-name']
#         contact_email = request.POST['contact-email']
#         contact_message = request.POST['contact-message']

#          #send an email
#         send_mail(
#             contact_name, #subject
#             contact_email, #message
#             contact_message, #from email
#             ['poozzaranna789@gmail.com'], #to email
#             )
#         return render(request, 'contact.html', {'contact_name':contact_name, 'contact_email': contact_email, 'contact_message': contact_message})  
#     else:
#         return render(request,'contact.html',{})  
    
# def gallery(request):
#     galleries = ImageGallery.objects.all()  
#     return render(request, 'gallery.html', {'galleries': galleries})    
     
# def menu(request):
#     menus = FoodMenu.objects.all()
#     return render(request, 'menu.html', {'menus': menus})    

# def opening(request):
#     return render(request, 'opening.html')    
    
# def services(request):
#     return render(request, 'services.html')    
    
# def about(request):
#     return render(request, 'about.html')    

# def home(request):
#     return render(request, 'home.html')    

def dashboard(request):
    menus = FoodMenu.objects.all()
    galleries = ImageGallery.objects.all()

    return render(request, 'dashboard.html', {'menus': menus, 'galleries': galleries})
    

    

    
