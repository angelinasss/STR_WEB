import re
from django.shortcuts import redirect, render, get_object_or_404
import requests
from .models import ArtType, Article, Cart, CartItem, CompanyInfo, FAQ, Employee, Job, Partners, Review, PromoCode, PrivacyPolicy, Hall, Position, Exhibit, Excursion, Exhibition, Ticket_Excursion, Ticket_Exhibition
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpRequest
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
import calendar
from datetime import date
from django.db.models import Q, Count
from django.urls import reverse
from django.http import JsonResponse
from decimal import Decimal
from django.db.models import Count, Sum, Avg, Max, DecimalField
from django.db.models.functions import Coalesce
from statistics import mode, median
import calendar
from django.db.models.functions import Cast
from django.contrib.contenttypes.models import ContentType

def home(request):
    latest_article = Article.objects.order_by('-published_at').first()
    
    year = datetime.now().year
    month = datetime.now().month
    cal = calendar.TextCalendar(calendar.SUNDAY)
    month_calendar = cal.formatmonth(year, month)
    company_info = CompanyInfo.objects.first()
    excursions = Excursion.objects.all()
    exhibitions = Exhibition.objects.all()
    partners = Partners.objects.all()

    weather_data = None
    city = None
    temperature = None
    description = None
    
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            is_employee = True
        except Employee.DoesNotExist:
            employee = None
            is_employee = False
        
        # Выполняем запрос к API только для авторизованных пользователей
        api_key = 'a1fcf314c6d72c6c6abfcd3396aab59b'
        city = request.GET.get('city', 'Minsk')  
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
        else:
            # Обработка ошибок API
            temperature = 'N/A'
            description = 'Error retrieving weather data'
    else:
        is_employee = False
        temperature = 'Login required to see weather data'
        description = ''
    
    context = {
        'title': 'Home',
        'article': latest_article,
        'city': city,
        'temperature': temperature,
        'description': description,
        'calendar': month_calendar,
        'is_employee': is_employee,
        'info' : company_info,
        'excursions' : excursions,
        'exhibitions' : exhibitions,  
        'partners' : partners,
        'year': year,
    }

    assert isinstance(request, HttpRequest)
    return render(request, 'app/index.html', context)


def contact(request):
    employees = Employee.objects.all()
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Employees',
            'employees': employees,
            'is_employee' : is_employee,
            'year':datetime.now().year,
        }
    )

def employee_list(request):
    sort_order = request.GET.get('sort', None)
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    if sort_order == 'asc':
        employees = Employee.objects.all().order_by('last_name')
    else:
        employees = Employee.objects.all()

    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'employees': employees,
            'is_employee' : is_employee,
            'year':datetime.now().year,
        }
    )
        
def contact_delete(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return HttpResponseRedirect("/contact/")

def about(request):
    company_info = CompanyInfo.objects.first()
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About Us',
            'info': company_info,
            'is_employee' : is_employee,
            'year':datetime.now().year,
        }
    )

def edit_company_info(request):
    info = CompanyInfo.objects.first()

    if request.method == "POST":
        if not info:
            info = CompanyInfo()
        
        info.description = request.POST.get("description")
        if request.FILES.get('logo'):
            info.logo = request.FILES['logo']
        if 'video' in request.FILES:
                info.video = request.FILES['video']
        info.history = request.POST.get("history")
        info.details = request.POST.get("details")
        info.save()
        return HttpResponseRedirect("/about/")
    
    return render(request, 'app/edit_company_info.html', {'info': info, 'title':'Edit Company Information',})

def news(request):
    articles = Article.objects.all()
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/news.html',
        {
            'title':'News',
            'articles': articles,
            'is_employee' : is_employee,
            'year':datetime.now().year,
        }
    )

def create_article(request):
    if request.method == "POST":
        article = Article()
        article.title = request.POST.get("title")
        article.content = request.POST.get("content")
        article.short_description = request.POST.get("short_description")
        if request.FILES.get('image'):
            article.image = request.FILES['image']
        article.published_at = request.POST.get("published_at")
        article.save()
        return HttpResponseRedirect("/news/")
    else:
        return render(
            request,
            'app/create_article.html',
            {
                'title':'Create A News',
                'year':datetime.now().year,
            }
        )

def deleteArticle(request, id):
    try:
        article = Article.objects.get(id=id)
        article.delete()
        return HttpResponseRedirect("/news/")
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    
def editArticle(request, id):
    try:
        article = Article.objects.get(id=id)
 
        if request.method == "POST":
            article.title = request.POST.get("title")
            article.content = request.POST.get("content")
            article.short_description = request.POST.get("short_description")
            if request.FILES.get('image'):
                article.image = request.FILES['image']
            article.published_at = timezone.now()
            article.save()
            return HttpResponseRedirect("/news/")
        else:
            user_timezone = timezone.get_current_timezone()
            published_at_user_tz = article.published_at.astimezone(user_timezone)
            published_at_utc = article.published_at.astimezone(timezone.utc)
            
            formatted_published_at_user_tz = published_at_user_tz.strftime("%d/%m/%Y %H:%M:%S")
            formatted_published_at_utc = published_at_utc.strftime("%d/%m/%Y %H:%M:%S")
            
            return render(
                request,
                'app/editArticle.html',
                {
                    'title':'Edit News',
                    'article': article,
                    'published_at_user_tz': formatted_published_at_user_tz,
                    'published_at_utc': formatted_published_at_utc,
                    'user_timezone': user_timezone,
                    'year':datetime.now().year,
                }
            )
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    
def article_detail(request, id):
    article = Article.objects.get(id=id)
    
    published_at_utc = article.published_at
    published_at_local = timezone.localtime(article.published_at)
    
    published_at_utc_str = published_at_utc.strftime("%d %b %Y %H:%M")
    published_at_local_str = published_at_local.strftime("%d %b %Y %H:%M")
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    return render(
        request,
        'app/article_detail.html',
        {
            'title': article.title,
            'article': article,
            'is_employee' : is_employee,
            'published_at_utc' : published_at_utc_str,
            'published_at_local': published_at_local_str,
            'year': datetime.now().year,
        }
    )

def article_all(request, id):
    article = Article.objects.get(id=id)
    
    published_at_utc = article.published_at
    published_at_local = timezone.localtime(article.published_at)
    
    published_at_utc_str = published_at_utc.strftime("%d %b %Y %H:%M")
    published_at_local_str = published_at_local.strftime("%d %b %Y %H:%M")
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    return render(
        request,
        'app/article_all.html',
        {
            'title': article.title,
            'article': article,
            'is_employee' : is_employee,
            'published_at_utc' : published_at_utc_str,
            'published_at_local': published_at_local_str,
            'year': datetime.now().year,
        }
    )

def faq(request):
    faqs = FAQ.objects.all()
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/faq.html',
        {
            'title':'FAQ',
            'faqs': faqs,
            'is_employee' : is_employee,
            'year':datetime.now().year,
        }
    )

def create_FAQ(request):
    if request.method == "POST":
        faq = FAQ()
        faq.question = request.POST.get("question")
        faq.answer = request.POST.get("answer")
        faq.added_date = request.POST.get("added_date")
        faq.save()
        return HttpResponseRedirect("/faq/")
    else:
        return render(
            request,
            'app/create_FAQ.html',
            {
                'title':'Create A FAQ',
                'year':datetime.now().year,
            }
        )

def delete_FAQ(request, id):
    try:
        faq = FAQ.objects.get(id=id)
        faq.delete()
        return HttpResponseRedirect("/faq/")
    except FAQ.DoesNotExist:
        return HttpResponseNotFound("<h2>FAQ not found</h2>")
    
def edit_FAQ(request, id):
     try:
        faq = FAQ.objects.get(id=id)
 
        if request.method == "POST":
            faq.question = request.POST.get("question")
            faq.answer = request.POST.get("answer")
            faq.added_date = timezone.now()
            faq.save()
            return HttpResponseRedirect("/faq/")
        else:
            return render(
                request,
                'app/edit_FAQ.html',
                {
                    'title':'Edit FAQ',
                    'faq': faq,
                    'year':datetime.now().year,
                }
            )
     except FAQ.DoesNotExist:
        return HttpResponseNotFound("<h2>FAQ not found</h2>")

def vacancies(request):
    jobs = Job.objects.all()
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/vacancies.html',
        {
            'title':'Vacancies',
            'jobs': jobs,
            'is_employee' : is_employee,
            'year':datetime.now().year,
        }
    )

def create_job(request):
    if request.method == "POST":
        vacancy = Job()
        vacancy.title = request.POST.get("title")
        vacancy.description = request.POST.get("description")
        vacancy.requirements = request.POST.get("requirements")
        vacancy.salary = request.POST.get("salary")
        vacancy.save()
        return HttpResponseRedirect("/vacancies/")
    else:
        return render(
            request,
            'app/create_vacancy.html',
            {
                'title':'Create A Vacancy',
                'year':datetime.now().year,
            }
        )

def delete_job(request, id):
    try:
        vacancy = Job.objects.get(id=id)
        vacancy.delete()
        return HttpResponseRedirect("/vacancies/")
    except Job.DoesNotExist:
        return HttpResponseNotFound("<h2>Vacancy not found</h2>")
    
def edit_job(request, id):
    try:
        vacancy = Job.objects.get(id=id)
 
        if request.method == "POST":
            vacancy.title = request.POST.get("title")
            vacancy.description = request.POST.get("description")
            vacancy.requirements = request.POST.get("requirements")
            vacancy.salary = request.POST.get("salary")
            vacancy.save()
            return HttpResponseRedirect("/vacancies/")
        else:
            return render(
                request,
                'app/edit_job.html',
                {
                    'title':'Vacancy Editing',
                    'vacancy': vacancy,
                    'year':datetime.now().year,
                }
            )
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h2>Vacancy not found</h2>")

def reviews(request):
    reviews = Review.objects.all()
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/reviews.html',
        {
            'title':'Reviews',
            'reviews': reviews,
            'is_employee' : is_employee,
            'year':datetime.now().year,
            'range_stars': range(1, 6)
        }
    )

def create_review(request):
     if request.method == "POST":
        review = Review()
        review.user = request.user
        review.rating = request.POST.get("rating")
        review.text = request.POST.get("text")
        review.created_at = timezone.now()
        review.save()
        return HttpResponseRedirect("/reviews/")

def delete_review(request, id):
    review = Review.objects.get(id=id)
    if review.user != request.user:
        return HttpResponseRedirect("/reviews/")  
    review.delete()
    return HttpResponseRedirect("/reviews/")

def edit_review(request, id):
    review = Review.objects.get(id=id)
 
    if request.method == "POST":
        review.rating = request.POST.get("rating")
        review.text = request.POST.get("text")
        review.created_at = timezone.now()
        review.save()
        return HttpResponseRedirect("/reviews/")
    else:
        return render(
            request,
            'app/edit_review.html',
            {
                'title':'Review Editing',
                'review': review,
                'year':datetime.now().year,
            }
        )

def privacy_policy(request):
    policy = PrivacyPolicy.objects.first()
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/privacy_policy.html',
        {
            'title':'Privacy Policy',
            'policy': policy,
            'is_employee' : is_employee,
            'year':datetime.now().year,
        }
    )

def promo_codes(request):
    all_promo_codes = PromoCode.objects.all()

    today = timezone.now().date()
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    for promo_code in all_promo_codes:
        if promo_code.expiration_date < today:
            if promo_code.is_active:
                promo_code.is_active = False
                promo_code.save()
                
    active_promo_codes = PromoCode.objects.filter(is_active=True)
    expired_promo_codes = PromoCode.objects.filter(is_active=False)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/promo_codes.html',
        {
            'title':'Promo Codes',
            'active_promo_codes': active_promo_codes,
            'expired_promo_codes': expired_promo_codes,
            'is_employee' : is_employee,
            'year':datetime.now().year,
        }
    )

def create_promo_code(request):
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        expiration_date = request.POST['expiration_date']
        
        expiration_date_obj = timezone.datetime.strptime(expiration_date, '%Y-%m-%d').date()

        is_active = expiration_date_obj >= timezone.now().date()

        PromoCode.objects.create(
            code=code,
            discount=discount,
            expiration_date=expiration_date,
            is_active=is_active
        )
        return HttpResponseRedirect("/promo_codes/")
    
    return render(
        request,
        'app/create_promo_code.html',
        {
            'title':'Create Promo Code',
            'year':datetime.now().year,
        }
    )

def edit_promo_code(request, id):
    promo_code = PromoCode.objects.get(id=id)
    
    if request.method == 'POST':
        promo_code.code = request.POST['code']
        promo_code.discount = request.POST['discount']
        promo_code.expiration_date = request.POST['expiration_date']
        
        expiration_date_obj = timezone.datetime.strptime(promo_code.expiration_date, '%Y-%m-%d').date()

        promo_code.is_active = expiration_date_obj >= timezone.now().date()
        promo_code.save()
        return HttpResponseRedirect("/promo_codes/")
    
    return render(
                request,
                'app/edit_promo_code.html',
                {
                    'title':'Promo Code Editing',
                    'promo_code': promo_code,
                    'year':datetime.now().year,
                }
            )

def delete_promo_code(request, id):
    try:
        promo_code = PromoCode.objects.get(id=id)
        promo_code.delete()
        return HttpResponseRedirect("/promo_codes/")
    except PromoCode.DoesNotExist:
        return HttpResponseNotFound("<h2>Promo Code not found</h2>")
    
def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        position_id = request.POST.get('position')
        hall_id = request.POST.get('hall')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        photo = request.FILES.get('photo')
        
        is_employee = 'is_employee' in request.POST
        
        positions = Position.objects.all()
        halls = Hall.objects.all()

        errors = {}
        
        if int(age) < 18:
            errors['age'] = 'You must be at least 18 years old.'

        if password != password_confirm:
            errors['password'] = 'Passwords do not match'
        
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists'

        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists'
            
        phone_pattern = re.compile(r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$')
        if is_employee:
            if not phone_pattern.match(phone):
                errors['phone'] = 'Phone number must be in the format +375 (XX) XXX-XX-XX'

        if errors:
            return render(request, 'app/register.html', {
                'error': 'Please correct the errors above.',
                'errors': errors,
                'positions': positions,
                'halls': halls,
                'form_data': request.POST, 
            })
        
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        
        if is_employee:
            position = Position.objects.get(id=position_id) if position_id else None
            hall = Hall.objects.get(id=hall_id) if hall_id else None
            Employee.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                position=position,
                hall=hall,
                photo=photo
            )
        else:
            Cart.objects.create(user=user)
        
        login(request, user)
        return HttpResponseRedirect("/")

    else:
        positions = Position.objects.all()
        halls = Hall.objects.all()
        return render(request, 'app/register.html', {
            'title': 'Registration',
            'positions': positions,
            'halls': halls,
            'year':datetime.now().year,
        })
    
@login_required
def profile(request, id):
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False
    
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        if employee:       
               employee.first_name = request.POST.get('first_name')
               user.first_name = request.POST.get('first_name')
               employee.last_name = request.POST.get('last_name')
               user.last_name = request.POST.get('last_name')
               employee.phone = request.POST.get('phone')
               employee.email = request.POST.get('email')
               user.email = request.POST.get('email')
               position_id = request.POST.get('position')
               hall_id = request.POST.get('hall')

               # Handle photo upload
               if 'photo' in request.FILES:
                   photo = request.FILES['photo']
                   employee.photo = photo
        
               # Set foreign keys
               if position_id:
                   employee.position = Position.objects.get(id=position_id)
               if hall_id:
                   employee.hall = Hall.objects.get(id=hall_id)

               employee.save()
               user.save()
           
               # Add a success message
               messages.success(request, 'Your profile has been updated successfully.')
           
               positions = Position.objects.all()
               halls = Hall.objects.all()

               return render(request, 'app/profile.html', {
                    'title': 'Profile',
                    'employee': employee,
                    'positions': positions,
                    'halls': halls,
                    'year':datetime.now().year,
                    'is_employee' : is_employee,
               })
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        user.save()
        
        # Add a success message
        messages.success(request, 'Your profile has been updated successfully.')

        return render(request, 'app/profile.html', {
            'title': 'Profile',
            'user' : user,
            'year':datetime.now().year,
            'is_employee' : is_employee,
        })

    positions = Position.objects.all()
    halls = Hall.objects.all()


    if employee: 
        return render(request, 'app/profile.html', {
            'title': 'Profile',
            'employee': employee,
            'positions': positions,
            'halls': halls,
            'year':datetime.now().year,
            'is_employee' : is_employee,
        })
    
    return render(request, 'app/profile.html', {
           'title': 'Profile',
           'user': user,
           'year':datetime.now().year,
           'is_employee' : is_employee,
       })

def hall_info(request):
    # Получаем все залы
    halls = Hall.objects.all()

    # Получаем параметр сортировки из запроса GET
    sort_by = request.GET.get('sort_by', 'name_asc')

    # Применяем сортировку
    if sort_by == 'name_asc':
        halls = halls.order_by('name')
    elif sort_by == 'name_desc':
        halls = halls.order_by('-name')
    elif sort_by == 'number_asc':
        halls = halls.order_by('number')
    elif sort_by == 'number_desc':
        halls = halls.order_by('-number')
    elif sort_by == 'area_asc':
        halls = halls.order_by('area')
    elif sort_by == 'area_desc':
        halls = halls.order_by('-area')
    elif sort_by == 'floor_asc':
        halls = halls.order_by('floor')
    elif sort_by == 'floor_desc':
        halls = halls.order_by('-floor')

    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            is_employee = True
        except Employee.DoesNotExist:
            is_employee = False
    else:
        is_employee = False

    # Возвращаем ответ с отсортированными залами
    return render(request, 'app/hall_info.html', {
        'title': 'Museum Halls',
        'halls': halls,
        'is_employee': is_employee,
        'sort_by': sort_by,  # Передаем выбранную сортировку в шаблон
        'year': datetime.now().year,
    })

def edit_hall(request, id):
    
    hall = Hall.objects.get(id=id)
    
    if request.method == 'POST':
       
        number = request.POST.get("number")
        name = request.POST.get("name")
        floor = request.POST.get("floor")
        area = request.POST.get("area")

        if Hall.objects.filter(Q(number=number) & ~Q(id=id)).exists():
            messages.error(request, 'A hall with this number already exists. Please choose a different number.')
        else:
            hall.number = number
            messages.success(request, 'Hall information has been updated successfully.')
            
        hall.name = name
        hall.floor = floor
        hall.area = area
        hall.save()

        return render(
            request,
            'app/edit_hall.html',
            {
                'title':'Edit Hall Information',
                'hall': hall,
                'year':datetime.now().year,
            }
        )

    else:
        
        return render(
            request,
            'app/edit_hall.html',
            {
                'title':'Edit Hall Information',
                'hall': hall,
                'year':datetime.now().year,
            }
        )
    
def create_hall(request):
   if request.method == 'POST':
        
        if Hall.objects.filter(Q(number=request.POST.get("number"))).exists():
            messages.error(request, 'A hall with this number already exists. Please choose a different number.')
            
            return render(
                request,
                'app/create_hall.html',
                {
                    'title':'Create A Hall',
                    'name' : request.POST.get("name"),
                    'floor' : request.POST.get("floor"),
                    'area' : request.POST.get("area"),
                    'year':datetime.now().year,
                }
            )
        else:
            hall = Hall()
            hall.number = request.POST.get("number")
            hall.name = request.POST.get("name")
            hall.floor = request.POST.get("floor")
            hall.area = request.POST.get("area")
            hall.save()
            
            messages.success(request, 'Hall has been created successfully.')
        
            return render(
                request,
                'app/create_hall.html',
                {
                    'title':'Create A Hall',
                    'year':datetime.now().year,
                }
            )
   else:
        return render(
            request,
            'app/create_hall.html',
            {
                'title':'Create A Hall',
                'year':datetime.now().year,
            }
        )
    
def delete_hall(request, id):
    hall = Hall.objects.get(id=id)
    
    Employee.objects.filter(hall=hall).update(hall=None)
    
    Exhibit.objects.filter(hall=hall).delete()

    hall.delete()
    halls = Hall.objects.all()
    return render(request, 'app/hall_info.html', {
            'title': 'Delete A Hall',
            'halls': halls,
            'year':datetime.now().year,
        })
    
def hall_detail(request, id):
    
    hall = Hall.objects.get(id=id)
        
    exhibits = Exhibit.objects.filter(hall=hall)
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False
        
    return render(request, 'app/hall_detail.html', {
        'title': 'Hall Information',
        'exhibits': exhibits,
        'hall' : hall,
        'is_employee' : is_employee,
        'year':datetime.now().year,
    })

def edit_exhibit(request, id):
    
    exhibit = Exhibit.objects.get(id=id)
    halls = Hall.objects.all()
    caretakers = Employee.objects.all()
    art_types = ArtType.objects.all()
    
    if request.method == 'POST':
       
        exhibit.name = request.POST.get("name")
        exhibit.art_type = ArtType.objects.get(id=request.POST.get("art_type"))
        exhibit.date_acquired = request.POST['date_acquired']
        exhibit.hall = Hall.objects.get(id=request.POST.get("hall"))
        if request.FILES.get('image'):
               exhibit.image = request.FILES['image']
        exhibit.caretaker = Employee.objects.get(id=request.POST.get("caretaker"))
        exhibit.save()

        messages.success(request, 'Exhibit information has been updated successfully.')    
        
        exhibit.refresh_from_db()

        return render(
            request,
            'app/edit_exhibit.html',
            {
                'title':'Edit Exhibit Information',
                'exhibit': exhibit,
                'halls' : halls,
                'caretakers' : caretakers,
                'art_types' : art_types,
                'year' : datetime.now().year,
            }
        )

    else:
        
        return render(
            request,
            'app/edit_exhibit.html',
            {
                'title':'Edit Exhibit Information',
                'exhibit': exhibit,
                'halls' : halls,
                'caretakers' : caretakers,
                'art_types' : art_types,
                'year':datetime.now().year,
            }
        )
    
def create_exhibit(request, id):
   
   hall = Hall.objects.get(id=id)
   
   if request.method == 'POST':
        
        exhibit = Exhibit()
        exhibit.hall = hall
        exhibit.name = request.POST.get("name")
        exhibit.art_type = ArtType.objects.get(id=request.POST.get("art_type"))
        exhibit.date_acquired = request.POST.get("date_acquired")
        exhibit.caretaker = Employee.objects.get(id=request.POST.get("caretaker"))
        if request.FILES.get('image'):
           exhibit.image = request.FILES['image']
        exhibit.save()
            
        messages.success(request, 'Exhibit has been created successfully.')
        
        return render(
            request,
            'app/create_exhibit.html',
            {
                'title':'Create An Exhibit',
                'year':datetime.now().year,
            }
        )
   else:
        art_types = ArtType.objects.all()
        caretakers = Employee.objects.all()
       
        return render(
            request,
            'app/create_exhibit.html',
            {
                'title':'Create An Exhibit',
                'hall' : hall,
                'art_types' : art_types,
                'caretakers' : caretakers,
                'year':datetime.now().year,
            }
        )
    
def delete_exhibit(request, id):
    exhibit = Exhibit.objects.get(id=id)
    
    hall = exhibit.hall

    exhibit.delete()
        
    exhibits = Exhibit.objects.filter(hall=hall)
        
    return render(request, 'app/hall_detail.html', {
        'title': 'Hall Information',
        'exhibits': exhibits,
        'hall' : hall,
        'year':datetime.now().year,
    })

def newest_exhibits(request):
    
    now = timezone.now()
    six_months_ago = now - timedelta(days=6*30)

    exhibits = Exhibit.objects.filter(date_acquired__range=[six_months_ago, now])
        
    return render(request, 'app/newest_exhibits.html', {
        'title': 'Exhibits received by the museum over the past six months',
        'exhibits': exhibits,
        'year':datetime.now().year,
    })

def create_new_exhibit(request):
   art_types = ArtType.objects.all()
   caretakers = Employee.objects.all()
   halls = Hall.objects.all()
   
   if request.method == 'POST':
        
        exhibit = Exhibit()
        exhibit.hall = Hall.objects.get(id=request.POST.get("hall"))
        exhibit.name = request.POST.get("name")
        exhibit.art_type = ArtType.objects.get(id=request.POST.get("art_type"))
        exhibit.date_acquired = request.POST.get("date_acquired")
        if request.FILES.get('image'):
           exhibit.image = request.FILES['image']
        exhibit.caretaker = Employee.objects.get(id=request.POST.get("caretaker"))
        
        exhibit.save()
            
        messages.success(request, 'Exhibit has been created successfully.')
        
        return render(
            request,
            'app/create_new_exhibit.html',
            {
                'title':'Create An Exhibit',
                'art_types' : art_types,
                'caretakers' : caretakers,
                'halls' : halls,
                'year':datetime.now().year,
            }
        )
   else:
       
        return render(
            request,
            'app/create_new_exhibit.html',
            {
                'title':'Create An Exhibit',
                'art_types' : art_types,
                'caretakers' : caretakers,
                'halls' : halls,
                'year': datetime.now().year,
            }
        )
   
def employees_by_floor(request):
    floors = Hall.objects.values_list('floor', flat=True).distinct() 

    if request.method == 'POST':
        
         selected_floor = request.POST.get('floor')
         employees = None

         if selected_floor is not None:
            employees = Employee.objects.filter(
                hall__floor=selected_floor
            ).distinct()

         return render(
            request,
            'app/employees_by_floor.html',
            {
                'title':'Employees By Floor',
                'employees': employees,
                'selected_floor': selected_floor,
                'floors' : floors,
                'year': datetime.now().year,
            }
         )
    else:
       
        return render(
            request,
            'app/employees_by_floor.html',
            {
                'title':'Employees By Floor',
                'floors' : floors,
                'year': datetime.now().year,
            }
        )

def exhibits_by_arrival_date(request):
    halls_with_counts = []
    selected_date = None

    if request.method == 'POST':
        selected_date = request.POST.get('date')

        if selected_date:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
            
            halls_with_counts = Hall.objects.annotate(
                exhibit_count=Count('exhibit', filter=Q(exhibit__date_acquired__gt=selected_date))
            ).filter(exhibit_count__gt=0)
            
        return render(
        request,
        'app/exhibits_by_arrival_date.html',
        {
            'title': 'Exhibits By Arrival Date',
            'halls_with_counts': halls_with_counts,
            'selected_date': selected_date,
            'year': datetime.now().year,
        }
    )
            
    else:
        return render(
        request,
        'app/exhibits_by_arrival_date.html',
        {
            'title': 'Exhibits By Arrival Date',
            'halls_with_counts': halls_with_counts,
            'year': datetime.now().year,
        }
    )
    
def excursions_by_season(request):
    season = None
    excursions = []
    total_excursions = 0

    if request.method == 'POST':
        season = request.POST.get('season')

        if season == 'winter':
            excursions = Excursion.objects.filter(
                Q(date__month=12, date__day__gte=1) | 
                Q(date__month=1, date__day__gte=1) |
                Q(date__month=2, date__day__lte=28)
            )
            
        elif season == 'spring':
            excursions = Excursion.objects.filter(
                Q(date__month__gte=3, date__month__lte=5) &
                Q(date__day__gte=1, date__day__lte=31)
            )
            
        elif season == 'summer':
            excursions = Excursion.objects.filter(
                Q(date__month__gte=6, date__month__lte=8) &
                Q(date__day__gte=1, date__day__lte=31)
            )
            
        elif season == 'autumn':
            excursions = Excursion.objects.filter(
                Q(date__month__gte=9, date__month__lte=11) &
                Q(date__day__gte=1, date__day__lte=30)
            )
            
        total_excursions = excursions.count()
            
        return render(
        request,
        'app/excursions_by_season.html',
        {
            'title': 'Excursions by Season',
            'excursions': excursions,
            'total_excursions': total_excursions,
            'selected_season': season,
            'year': datetime.now().year,
        }
    )
            
    else:
        return render(
        request,
        'app/excursions_by_season.html',
        {
            'title': 'Excursions by Season',
            'excursions': excursions,
            'total_excursions': total_excursions,
            'year': datetime.now().year,
        }
    )
    
def create_excursion(request):
    exhibits = Exhibit.objects.all()
    guides = Employee.objects.filter(position__name='Guide')
    

    if request.method == "POST":
        item_type = request.POST.get('item_type')
        
        if item_type == 'excursion':
            code = request.POST.get('code')
            name = request.POST.get('excursion_name')
            date = request.POST.get('date')
            season = request.POST.get('season')
            group_size = request.POST.get('group_size')
            guide = Employee.objects.get(id=request.POST.get("guide"))
            price = request.POST.get('excursion_price')
            
            excursion = Excursion.objects.create(
                code=code,
                name=name,
                date=date,
                season=season,
                group_size=group_size,
                guide=guide,
                price=price
            )
            excursion.save()
            
            messages.success(request, 'Excursion has been created successfully.')
            
            return render(
            request,
            'app/create_excursion.html',
            {
                'title':'Create An Excursion/Exhibition',
                'item_type': item_type,
                'exhibits': exhibits,
                'guides' : guides,
                'year':datetime.now().year,
            }
        )

        elif item_type == 'exhibition':
            name = request.POST.get('exhibition_name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            exhibits_ids = request.POST.getlist('exhibits_list[]')
            exhibitss = Exhibit.objects.filter(id__in=exhibits_ids)
            price = request.POST.get('exhibition_price')
            
            exhibition = Exhibition.objects.create(
                name=name,
                start_date=start_date,
                end_date=end_date,
                price=price
            )
            exhibition.exhibits.set(exhibitss)
            exhibition.save()
            
            messages.success(request, 'Exhibition has been created successfully.')
            
            return render(
            request,
            'app/create_excursion.html',
            {
                'title':'Create An Excursion/Exhibition',
                'item_type': item_type,
                'exhibits': exhibits,
                'guides' : guides,
                'year':datetime.now().year,
            }
        )
    else:
        item_type = request.GET.get('item_type', 'excursion')
        
        return render(
            request,
            'app/create_excursion.html',
            {
                'title':'Create An Excursion/Exhibition',
                'item_type': item_type,
                'exhibits': exhibits,
                'guides' : guides,
                'year':datetime.now().year,
            }
        )
    
def excursion_delete(request, id):
    season = request.GET.get('seasonn')
     
    if request.method == 'POST':
        excursion = get_object_or_404(Excursion, id=id)
    
        excursion.delete()

    excursions = []
    total_excursions = 0
    
    if season == 'winter':
        excursions = Excursion.objects.filter(
        Q(date__month=12, date__day__gte=1) | 
        Q(date__month=1, date__day__gte=1) |
        Q(date__month=2, date__day__lte=28)
    )
    elif season == 'spring':
        excursions = Excursion.objects.filter(
        Q(date__month__gte=3, date__month__lte=5) &
        Q(date__day__gte=1, date__day__lte=31)
    )
    elif season == 'summer':
        excursions = Excursion.objects.filter(
        Q(date__month__gte=6, date__month__lte=8) &
        Q(date__day__gte=1, date__day__lte=31)
    )
    elif season == 'autumn':
        excursions = Excursion.objects.filter(
        Q(date__month__gte=9, date__month__lte=11) &
        Q(date__day__gte=1, date__day__lte=30)
    )
            
    total_excursions = excursions.count()
    
    return redirect(reverse('excursions_by_season') + f'?seasonn={season}')

def excursion_edit(request, id):
    excursion = Excursion.objects.get(id=id)
    guides = Employee.objects.filter(position__name='Guide')
    
    if request.method == 'POST':
       
        excursion.code = request.POST.get('code')
        excursion.name = request.POST.get('excursion_name')
        excursion.date = request.POST.get('date')
        excursion.season = request.POST.get('season')
        excursion.group_size = request.POST.get('group_size')
        excursion.guide = Employee.objects.get(id=request.POST.get("guide"))
        excursion.price = request.POST.get('price')
        
        excursion.save()
            
        messages.success(request, 'Excursion has been updated successfully.')
        
        excursion.refresh_from_db()

        return render(
            request,
            'app/excursion_edit.html',
            {
                'title':'Edit Exhibit Information',
                'excursion': excursion,
                'guides' : guides,
                'year' : datetime.now().year,
            }
        )

    else:
        
        return render(
            request,
            'app/excursion_edit.html',
            {
                'title':'Edit Exhibit Information',
                'excursion': excursion,
                'guides' : guides,
                'year':datetime.now().year,
            }
        )
    
def my_exhibits(request):
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False
       
    user = request.user
    employee = Employee.objects.get(user=user)
    exhibits = Exhibit.objects.filter(caretaker=employee).order_by('hall')
            
    return render(
        request,
        'app/my_exhibits.html',
        {
            'title': 'My Exhibits',
            'exhibits': exhibits,
            'is_employee' : is_employee,
            'year': datetime.now().year,
        }
    )

def my_excursions(request):
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False

    user = request.user
    employee = Employee.objects.get(user=user)
    excursions = Excursion.objects.filter(guide=employee)
            
    return render(
        request,
        'app/my_excursions.html',
        {
            'title': 'My Excursions',
            'excursions': excursions,
            'is_employee' : is_employee,
            'guide' : employee,
            'year': datetime.now().year,
        }
    )

def all_excursions(request):
    current_date = timezone.now().date()
    excursions = Excursion.objects.filter(date__gte=current_date)

    sort_by = request.GET.get('sort_by', None)
    
    if sort_by == 'date_asc':
        excursions = excursions.order_by('date')
    elif sort_by == 'date_desc':
        excursions = excursions.order_by('-date')
    elif sort_by == 'name_asc':
        excursions = excursions.order_by('name')
    elif sort_by == 'name_desc':
        excursions = excursions.order_by('-name')
    elif sort_by == 'price_asc':
        excursions = excursions.order_by('price')
    elif sort_by == 'price_desc':
        excursions = excursions.order_by('-price')

    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            is_employee = True
        except Employee.DoesNotExist:
            is_employee = False
    else:
        is_employee = False
            
    return render(
        request,
        'app/all_excursions.html',
        {
            'title': 'Excursions',
            'is_employee': is_employee,
            'excursions': excursions,
            'sort_by' : sort_by,
            'year': datetime.now().year,
        }
    )

from django.shortcuts import render
from django.utils import timezone
from .models import Exhibition
from datetime import datetime

def all_exhibitions(request):
    current_date = timezone.now().date()
    exhibitions = Exhibition.objects.filter(end_date__gte=current_date)

    # Get the sort option from the request
    sort_by = request.GET.get('sort_by', None)
    
    # Apply sorting based on the query parameter
    if sort_by == 'date_asc':
        exhibitions = exhibitions.order_by('start_date')
    elif sort_by == 'date_desc':
        exhibitions = exhibitions.order_by('-start_date')
    elif sort_by == 'name_asc':
        exhibitions = exhibitions.order_by('name')
    elif sort_by == 'name_desc':
        exhibitions = exhibitions.order_by('-name')
    elif sort_by == 'price_asc':
        exhibitions = exhibitions.order_by('price')
    elif sort_by == 'price_desc':
        exhibitions = exhibitions.order_by('-price')

    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            is_employee = True
        except Employee.DoesNotExist:
            is_employee = False
    else:
        is_employee = False
            
    return render(
        request,
        'app/all_exhibitions.html',
        {
            'title': 'Exhibitions',
            'is_employee': is_employee,
            'exhibitions': exhibitions,
            'sort_by' : sort_by,
            'year': datetime.now().year,
        }
    )

@login_required
def purchase_ticket_exhibition(request, id):
    exhibition = Exhibition.objects.get(id=id)
    
    promo_code_input = request.POST.get('promo_code', '').strip()

    promo_code = None
    total_price = exhibition.price
    
    if promo_code_input:
        try:
            promo_code = PromoCode.objects.get(
                code=promo_code_input,
                is_active=True,
                expiration_date__gte=date.today()
            )
            total_price = exhibition.price - exhibition.price * promo_code.discount * Decimal('0.01')
        except PromoCode.DoesNotExist:
            promo_code = None
            
    ticket = Ticket_Exhibition.objects.create(
        visitor=request.user,
        exhibition=exhibition,
        purchase_date=timezone.now(),
        promo_code=promo_code,
        total_price = total_price
    )
    return render(
    request,
    'app/ticket_success.html',
    {
        'title': 'Ticket Purchase',
        'year': datetime.now().year,
    }
    )

@login_required
def purchase_ticket_excursion(request, id):
    excursion = Excursion.objects.get(id=id)
    promo_code_input = request.POST.get('promo_code', '').strip()

    promo_code = None
    total_price = excursion.price
    
    if promo_code_input:
        try:
            promo_code = PromoCode.objects.get(
                code=promo_code_input,
                is_active=True,
                expiration_date__gte=date.today()
            )
            total_price = excursion.price - excursion.price * promo_code.discount * Decimal('0.01')
        except PromoCode.DoesNotExist:
            promo_code = None

    ticket = Ticket_Excursion.objects.create(
        visitor=request.user,
        excursion=excursion,
        promo_code=promo_code,
        total_price = total_price,
        purchase_date=timezone.now()
    )
    return render(
    request,
    'app/ticket_success_excursion.html',
    {
        'title': 'Ticket Purchase',
        'year': datetime.now().year,
    }
    )

@login_required
def my_tickets(request):
    tickets_excursions = Ticket_Excursion.objects.filter(visitor=request.user)
    tickets_exhibitions = Ticket_Exhibition.objects.filter(visitor=request.user)
    
    return render(
    request,
    'app/my_tickets.html',
    {
        'title': 'My Tickets',
        'tickets_excursions' : tickets_excursions,
        'tickets_exhibitions' : tickets_exhibitions,
        'year': datetime.now().year,
    }
    )

from django.shortcuts import render
from .models import Exhibit

def all_exhibits(request):
    exhibits = Exhibit.objects.all()

    # Получение параметра сортировки из GET-запроса
    sort_by = request.GET.get('sort_by', 'name_asc')

    # Применение сортировки
    if sort_by == 'name_asc':
        exhibits = exhibits.order_by('name')
    elif sort_by == 'name_desc':
        exhibits = exhibits.order_by('-name')
    elif sort_by == 'date_asc':
        exhibits = exhibits.order_by('date_acquired')
    elif sort_by == 'date_desc':
        exhibits = exhibits.order_by('-date_acquired')
    elif sort_by == 'hall_asc':
        exhibits = exhibits.order_by('hall')
    elif sort_by == 'hall_desc':
        exhibits = exhibits.order_by('-hall')

    # Проверка авторизации пользователя
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            is_employee = True
        except Employee.DoesNotExist:
            is_employee = False
    else:
        is_employee = False

    return render(
        request,
        'app/all_exhibits.html',
        {
            'title': 'Exhibits',
            'exhibits': exhibits,
            'is_employee': is_employee,
            'sort_by': sort_by,  # Передаем выбранное значение сортировки в шаблон
            'year': datetime.now().year,
        }
    )

@login_required
def nationality_by_name(request):
    name = request.user.first_name  

    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            is_employee = True
        except Employee.DoesNotExist:
            is_employee = False
    else:
        is_employee = False
    
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)
    
    nationalize_url = f'https://api.nationalize.io/?name={name}'
    
    try:
        # Получаем вероятность национальности
        nationalize_response = requests.get(nationalize_url)
        nationalize_response.raise_for_status()
        nationalize_data = nationalize_response.json()
        
        # Получаем коды стран из данных
        countries = nationalize_data.get('country', [])
        country_codes = [country.get('country_id') for country in countries]
        
        # Если коды стран есть, получаем полные названия стран
        if country_codes:
            rest_countries_url = f'https://restcountries.com/v3.1/all'
            rest_countries_response = requests.get(rest_countries_url)
            rest_countries_response.raise_for_status()
            rest_countries_data = rest_countries_response.json()
            
            # Создаём словарь для сопоставления кода страны с полным названием
            country_name_mapping = {country['cca2']: country['name']['common'] for country in rest_countries_data}
            
            # Формируем результат с полными названиями стран
            result = [
                {
                    'country_code': country.get('country_id'),
                    'country_name': country_name_mapping.get(country.get('country_id'), 'Unknown'),
                    'probability': country.get('probability')
                }
                for country in countries
            ]
        else:
            result = []
        
        return render(request, 'app/nationality.html', {'name': name, 'nationalities': result, 'title' : 'Nationality By Name', 'is_employee': is_employee})
    
    except requests.RequestException as e:
        return render(request, 'app/nationality.html', {'error': str(e), 'title' : 'Nationality By Name', 'is_employee': is_employee})
    
def statistics(request):
    context = {}

    # Check if the user has selected to view excursion or exhibition sales
    sale_type = request.GET.get('sale_type', 'Excursion')  # Default to excursions
    
    total_tickets_sold = 0;
    if sale_type == 'Excursion':
        tickets = Ticket_Excursion.objects.all()
        excursions = Excursion.objects.all()
        total_tickets_sold = tickets.count;
        labels = list(excursions.values_list('name', flat=True))
        sales_data =  [
            Ticket_Excursion.objects.filter(excursion=excursion).count() for excursion in excursions
            ]
        context['sales_type'] = 'Excursion'
    else:
        tickets = Ticket_Exhibition.objects.all()
        exhibitions = Exhibition.objects.all()
        total_tickets_sold = tickets.count;
        labels = list(exhibitions.values_list('name', flat=True))
        sales_data =  [
            Ticket_Exhibition.objects.filter(exhibition=exhibition).count() for exhibition in exhibitions
            ]
        context['sales_type'] = 'Exhibition'
    
    excursions_count = Ticket_Excursion.objects.count();
    exhibitions_count = Ticket_Exhibition.objects.count();
    sales_data_all = [excursions_count, exhibitions_count]

    # Calculate total sales sum
    total_sales = tickets.aggregate(
        total=Sum(Cast('total_price', output_field=DecimalField()))
    )['total']
    
    # Get list of sales for statistics calculation
    sales_list = list(tickets.values_list('total_price', flat=True))

    if sales_list:
        avg_sales = sum(sales_list) / len(sales_list)  # Average
        med_sales = median(sales_list)  # Median

        try:
            mod_sales = mode(sales_list)  # Mode (most common value)
        except:
            mod_sales = None  # No unique mode

        # Get the most popular excursion or exhibition by counting tickets
        if sale_type == 'Excursion':
            most_popular = tickets.values('excursion__name').annotate(ticket_count=Count('id')).order_by('-ticket_count').first()
        else:
            most_popular = tickets.values('exhibition__name').annotate(ticket_count=Count('id')).order_by('-ticket_count').first()

    else:
        avg_sales = med_sales = mod_sales = None
        most_popular = None

    context.update({
        'total_sales': total_sales,
        'total_tickets_sold' : total_tickets_sold,
        'avg_sales': avg_sales,
        'med_sales': med_sales,
        'mod_sales': mod_sales,
        'most_popular': most_popular,
        'sales_type': sale_type,
        'sales_labels': labels,
        'sales_data': sales_data,
        'sales_data_all' : sales_data_all,
        'title' : 'Sales Statistics',
        'year': datetime.now().year,
    })

    return render(request, 'app/statistics.html', context)

def certificate_view(request):
    context = {
        'name': 'John Doe',
        'date': 'September 17, 2024',
        'course_title': 'Course Title',
        'company_name': 'Company Name',
    }
    return render(request, 'certificate.html', context)

def excursion_detail(request, id):
    
    excursion = Excursion.objects.get(id=id)
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False
        
    return render(request, 'app/excursion_detail.html', {
        'excursion': excursion,
        'is_employee' : is_employee,
        'year' : datetime.now().year,
        'title' : 'Excursion Information'
    })

def exhibition_detail(request, id):
    
    exhibition = Exhibition.objects.get(id=id)
    
    if request.user.is_authenticated:
        try:
           employee = Employee.objects.get(user=request.user)
           is_employee = True
        except Employee.DoesNotExist:
           employee = None
           is_employee = False
    else:
        is_employee = False
        
    return render(request, 'app/exhibition_detail.html', {
        'exhibition': exhibition,
        'is_employee' : is_employee,
        'year':datetime.now().year,
        'title' : 'Exhibition Information'
    })

def add_to_cart_excursion(request, id):
    excursion = Excursion.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    excursion_content_type = ContentType.objects.get_for_model(Excursion)
    
    cart_item, item_created = CartItem.objects.get_or_create(
        user=request.user,
        content_type=excursion_content_type,
        object_id=excursion.id,
        defaults={'quantity': 1}
    )
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    if cart_item not in cart.items.all():
        cart.items.add(cart_item)
    
    # Add success message
    messages.success(request, 'Ticket for current excursion successfully added to your cart.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_to_cart_exhibition(request, id):
    exhibition = Exhibition.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    exhibition_content_type = ContentType.objects.get_for_model(Exhibition)
    
    cart_item, item_created = CartItem.objects.get_or_create(
        user=request.user,
        content_type=exhibition_content_type,
        object_id=exhibition.id,
        defaults={'quantity': 1}
    )
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    if cart_item not in cart.items.all():
        cart.items.add(cart_item)
    
    # Add success message
    messages.success(request, 'Ticket for current exhibition successfully added to your cart.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def my_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None
    
    cart_items = CartItem.objects.filter(user=request.user)
    total_cost = cart.total_cost if cart else 0
    
    return render(request, 'app/my_cart.html', {
        'title' : 'My Cart',
        'cart': cart,
        'cart_items': cart_items,
        'total_cost': total_cost,
    })

def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)

    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    if cart.items.filter(id=cart_item.id).exists():
        cart.items.remove(cart_item)
        cart_item.delete()

    return redirect('my_cart')

@login_required
def increase_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    cart_item.quantity += 1
    cart_item.save()
    
    return redirect('my_cart')

@login_required
def decrease_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart.items.remove(cart_item)
        cart_item.delete()
    
    return redirect('my_cart')

@login_required
def pay_page(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    return render(request, 'app/pay_page.html', {
        'title' : 'Payment Page',
        'item': cart_item,
    })

def get_model_instance(cart_item):
    content_type = cart_item.content_type
    model_class = content_type.model_class()
    return model_class.objects.get(id=cart_item.object_id)

@login_required
def process_payment(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    instance = get_model_instance(item)
    total_price = 0
        
    if isinstance(instance, Excursion):
        excursion = Excursion.objects.get(id=item.object_id)
        total_price = excursion.price
    elif isinstance(instance, Exhibition):
        exhibition = Exhibition.objects.get(id=item.object_id)
        total_price = exhibition.price
    
    promo_code_input = request.POST.get('promo_code', '').strip()

    promo_code = None
    
    if promo_code_input:
        try:
            promo_code = PromoCode.objects.get(
                code=promo_code_input,
                is_active=True,
                expiration_date__gte=date.today()
            )
            total_price = total_price - total_price * promo_code.discount * Decimal('0.01')
        except PromoCode.DoesNotExist:
            promo_code = None
            
    if isinstance(instance, Excursion):
        ticket = Ticket_Excursion.objects.create(
        visitor=request.user,
        excursion=excursion,
        promo_code=promo_code,
        total_price = total_price,
        purchase_date=timezone.now()
 
    )
        
    elif isinstance(instance, Exhibition):
        ticket = Ticket_Exhibition.objects.create(
        visitor=request.user,
        exhibition=exhibition,
        purchase_date=timezone.now(),
        promo_code=promo_code,
        total_price = total_price
    )
        
    cart = get_object_or_404(Cart, user=request.user)

    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    if cart.items.filter(id=cart_item.id).exists():
        cart.items.remove(cart_item)
        cart_item.delete()

    if isinstance(instance, Excursion):
        return render(
        request,
        'app/ticket_success_excursion.html',
        {
            'title': 'Ticket Purchase',
            'year': datetime.now().year,
        }
        )

    else:
        return render(
        request,
        'app/ticket_success.html',
        {
            'title': 'Ticket Purchase',
            'year': datetime.now().year,
        }
        )