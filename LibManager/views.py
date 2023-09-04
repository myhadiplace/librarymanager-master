from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect,HttpResponse, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import NewBookForm,NewAuthorForm,NewUserForm,LoginUserForm,OtpLoginForm,BookFilterForm,NormalDateReseveForm,VipDateReseveForm
from .models import Book,Users,Reservation
from .services.otpservice import OTPManager,check_opt_limit
from .services.jwt_manage import generate_jwt_token,decode_jwt_token
from datetime import datetime,timedelta
from .services.reservations_service import off_check,free_check,cost_calculater
from pymongo import MongoClient

#repository import
from .repository.repository import get_user_by_username,get_book_by_filters,get_uesr_reserved_book
# Create your views here.

# mongodb configuration
cluster = "mongodb://localhost:27017"
client = MongoClient(cluster)
db = client.library
# db.book.delete_many({})

# otp manager class
manager = OTPManager()

def books_list(request):
    all_book = db.book.find()
    filter_form = BookFilterForm()
    token = request.COOKIES.get('jwt_token')
    decoded_token = decode_jwt_token(token)
    return render(request,'LibManager/home.html',{'books':all_book,'filter_form':filter_form,'decoded_token':decoded_token})


def add_book(request):
    if request.method == "POST":
        form = NewBookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/new-book",{'form':form})
    else:
        form = NewBookForm()
    return render(request,'LibManager/new_book_form.html',{"form":form}) 
    
def delete_book(request,id):
    if request.method == "POST":
        book = get_object_or_404(Book,pk=id)
        book.delete()
        return HttpResponseRedirect('/')
    
def add_author(request):
    if request.method == "POST":
        form = NewAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/new-author")
    else:
        form = NewAuthorForm()
    return render(request,'LibManager/new_author_form.html',{"form":form}) 
    

def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            #create session for user
            session_data = {'otp_code':0,'two_minutes_otp_counter':0,'one_hours_otp_counter':0,'last_time_code_send':datetime.now().isoformat()}
            request.session[f'user_{new_user.id}_data'] = session_data
            return HttpResponseRedirect("/")
    else:
        form = NewUserForm()
    return render(request,'LibManager/new_user_form.html',{"form":form})

def login_user(request):
    if request.method == "POST":
        print(request.POST)
        form = LoginUserForm(request.POST)
        if form.is_valid():
            form_username = form.cleaned_data['username']
            form_password = form.cleaned_data['password']

            user_obj = get_user_by_username(form_username)
            if user_obj['error']:
                return user_obj
            if user_obj.password == form_password: #validate user password
                #send otp code to user
                if check_opt_limit(request,user_obj.id):
                    # send otp code to user and save it in session for future use
                    otp_code = manager.send_opt(user_obj.id) 
                    request.session[f'{user_obj.id}_otp_code'] = otp_code
                    print(otp_code)
                    url = reverse("OtpAuth",kwargs={"user_id":user_obj.id})
                    response = HttpResponseRedirect(url)
                    return response
                else:
                    JsonResponse({'error': 'too many attempts'})
            else:
                return JsonResponse({'error':'invalid password'})
    else:
        #using decode jwt token that store in cookies we chack if user need to logge in or not
        jwt_token = request.COOKIES.get('jwt_token')
        logged_user_id = request.COOKIES.get('logged_user_id')
        if jwt_token:
            decoded_token = decode_jwt_token(jwt_token)
            if decoded_token and decoded_token['user_id'] == int(logged_user_id):
                return HttpResponse('you already logged in')
    form = LoginUserForm()
    return render (request,'LibManager/login_user_form.html',{"form":form})


def logout(request):
    token = request.COOKIES.get('jwt_token')
    logged_user_id = request.COOKIES.get('logged_user_id')
    if token:
        decoded_token = decode_jwt_token(token)
        if decoded_token and decoded_token['user_id'] == int(logged_user_id):
            # invalidate user token and remove from cookie
            valid_time = 1 
            generate_jwt_token(int(decoded_token['user_id']),valid_time)
            response =  HttpResponse("you successfuly loged out")
            response.set_cookie('jwt_token','')
            response.set_cookie('logged_user_id','')
            return response
        else:
            return HttpResponse('invalid token or user id')
    else:
        return HttpResponse('you must login')

def otp_authenticate(request,user_id):
    if request.method == "POST":
        form = OtpLoginForm(request.POST)
        actuall_otp_code = request.session.get(f'{user_id}_otp_code')
        form_otp_code = request.POST['otp_number_field'] 
        if form.is_valid(): 
                if actuall_otp_code == int(form_otp_code):
                    del request.session[f'{user_id}_otp_code']

                    #generate jwt code and store it in cookie
                    response = HttpResponseRedirect('/')
                    token = generate_jwt_token(user_id,86400)
                    print(token)
                    response.set_cookie('logged_user_id',user_id)
                    response.set_cookie('jwt_token',token)
                    return response
        
                else:
                    return HttpResponse("invalid otp code")
        else:
            return HttpResponse("invalid form")
    else:
        form  = OtpLoginForm()
        return render (request,'LibManager/otp_form.html',{"form":form,'user_id':user_id})


def search(request):
    if request.method == 'POST':
        query = request.POST['search_query']
        books = Book.objects.filter(title__contains=query)
        if books.exists():   
            return render (request,'LibManager/home.html',{'books':books})
        else:
            return JsonResponse({'error':'nothing founded'})

def book_filters(request):
    form = BookFilterForm(request.GET)
    if form.is_valid():
        genre = form.cleaned_data['geners']
        price_min = form.cleaned_data['price_min']
        price_max = form.cleaned_data['price_max']
        author_country = form.cleaned_data['author_country']

        # get books by filters
        filtered_books = get_book_by_filters(genre=genre, author_country=author_country,price_max=price_max,price_min=price_min)
        
        result = list(filtered_books.values())
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('invalid form')

def sorting(request):
    sort_type = request.GET['sort-type']
    if sort_type == 'descendig':
        books = Book.objects.all().order_by('-price')
    else:
        books = Book.objects.all().order_by('price')
    filter_form = BookFilterForm()
    return render (request,'LibManager/home.html',{'books':books,'filter_form':filter_form})



def reserve_book(request,user_id,book_id):
    try:
        user_obj = Users.objects.get(pk=user_id)
        book_obj = Book.objects.get(pk=book_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error':"objects not founded"})
        
    reserve_end = datetime.now().date() + timedelta(days=7)
    if request.method == "POST":
        reserve_day = request.POST['reserve_date']

        #calculate the cost for reserve book
        reserve_cost = cost_calculater(user_id=user_obj,reserve_day=reserve_day,membership_type=user_obj.membership_type)

        new_reserve = Reservation(user=user_obj,book=book_obj,reserve_end=reserve_end,cost=reserve_cost)

        new_reserve.save()
        data = request.POST
        
        response = HttpResponseRedirect(f'/pay/?book_title={data["book_name"]}&reserve_for={data["reserve_date"]}&reserve_cost={reserve_cost}')
        return response
    else:
        if user_obj.membership_type == 'vip':
            token = request.COOKIES.get('jwt_token') 
            initial_data = {'user_token':token,'book_name':book_obj.title}
            form = VipDateReseveForm(initial=initial_data)
            decoded_token = decode_jwt_token(token)  
            return render(request,'LibManager/reserve_book.html',{'form':form,"reserve_details":book_obj, 'decoded_token':decoded_token})
        else:
            token = request.COOKIES.get('jwt_token') 
            initial_data = {'user_token':token,'book_name':book_obj.title}
            form = NormalDateReseveForm(initial=initial_data)
            decoded_token = decode_jwt_token(token)  
        return render(request,'LibManager/reserve_book.html',{'form':form,"reserve_details":book_obj, 'decoded_token':decoded_token})


def payment(request):
    if request.method == 'POST':
        pass
    else:
        data = request.GET
        return render (request,'LibManager/pyment.html',{'submited_form_data':data})
    

def all_reserve_book(request,user_id):
    if request.method == "GET":
        token = request.COOKIES.get('jwt_token')
        decoded_token = decode_jwt_token(token)
        if decoded_token and decoded_token['user_id'] == user_id:
            result = list(get_uesr_reserved_book(user_id))
    return JsonResponse(result,safe=False)



