import re
from django.shortcuts import redirect, render, get_object_or_404
import requests
from .models import ArtType, Article, CompanyInfo, FAQ, Employee, Job, Review, PromoCode, PrivacyPolicy, Hall, Position, Exhibit, Excursion, Exhibition, Ticket_Excursion, Ticket_Exhibition
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpRequest
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
import calendar
from datetime import datetime
from django.db.models import Q, Count
from django.urls import reverse
from django.http import JsonResponse

def home(request):
    latest_article = Article.objects.order_by('-published_at').first()
    
    api_key = 'a1fcf314c6d72c6c6abfcd3396aab59b'
    city = request.GET.get('city', 'Minsk')  
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    response = requests.get(url)
    weather_data = response.json()
    
    year = datetime.now().year
    month = datetime.now().month
    cal = calendar.TextCalendar(calendar.SUNDAY)
    month_calendar = cal.formatmonth(year, month)
    
    context = {
        'title': 'Home',
        'article': latest_article,
        'city': city,
        'temperature': weather_data['main']['temp'],
        'description': weather_data['weather'][0]['description'],
        'calendar': month_calendar,
        'year': datetime.now().year,
    }

    assert isinstance(request, HttpRequest)
    return render(request, 'app/index.html', context)


def contact(request):
    employees = Employee.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'employees': employees,
            'year':datetime.now().year,
        }
    )

def contact_create(request):
     if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        position = Position.objects.get(id=request.POST.get('position'))
        hall = Hall.objects.get(id=request.POST.get('hall'))
        photo = request.FILES.get('photo')
        
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
        return HttpResponseRedirect("/contact/")
     else:
        halls = Hall.objects.all()
        positions = Position.objects.all()
    
        return render(
              request,
              'app/contact_create.html',
              {
                  'title':'Create Employee',
                  'halls' : halls,
                  'positions' : positions,
                  'year':datetime.now().year,
              }
        )
        
def contact_delete(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return HttpResponseRedirect("/contact/")

def about(request):
    company_info = CompanyInfo.objects.first()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'info': company_info,
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
        info.video = request.POST.get("video")
        info.history = request.POST.get("history")
        info.details = request.POST.get("details")
        info.save()
        return HttpResponseRedirect("/about/")
    
    return render(request, 'app/edit_company_info.html', {'info': info})

def news(request):
    articles = Article.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/news.html',
        {
            'title':'News',
            'articles': articles,
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
    return render(
        request,
        'app/article_detail.html',
        {
            'title': article.title,
            'article': article,
            'year': datetime.now().year,
        }
    )

def faq(request):
    faqs = FAQ.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/faq.html',
        {
            'title':'FAQ',
            'faqs': faqs,
            'year':datetime.now().year,
        }
    )

def create_FAQ(request):
    if request.method == 'POST':
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
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/vacancies.html',
        {
            'title':'Vacancies',
            'jobs': jobs,
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
                    'title':'Edit Vacancy',
                    'vacancy': vacancy,
                    'year':datetime.now().year,
                }
            )
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h2>Vacancy not found</h2>")

def reviews(request):
    reviews = Review.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/reviews.html',
        {
            'title':'Reviews',
            'reviews': reviews,
            'year':datetime.now().year,
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
                'title':'Edit Review',
                'review': review,
                'year':datetime.now().year,
            }
        )

def privacy_policy(request):
    policy = PrivacyPolicy.objects.first()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/privacy_policy.html',
        {
            'title':'Privacy Policy',
            'policy': policy,
            'year':datetime.now().year,
        }
    )

def promo_codes(request):
    all_promo_codes = PromoCode.objects.all()

    today = timezone.now().date()

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
                    'title':'Edit Promo Code',
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
    try:
       employee = Employee.objects.get(user=request.user)
       is_employee = True
    except Employee.DoesNotExist:
       employee = None
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

    halls = Hall.objects.all()
        
    return render(request, 'app/hall_info.html', {
        'title': 'Hall Information',
        'halls': halls,
        'year':datetime.now().year,
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
        
    return render(request, 'app/hall_detail.html', {
        'title': 'Hall Information',
        'exhibits': exhibits,
        'hall' : hall,
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
    try:
       employee = Employee.objects.get(user=request.user)
       is_employee = True
    except Employee.DoesNotExist:
       employee = None
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
    try:
       employee = Employee.objects.get(user=request.user)
       is_employee = True
    except Employee.DoesNotExist:
       employee = None
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
            
    return render(
        request,
        'app/all_excursions.html',
        {
            'title': 'Excursions',
            'excursions': excursions,
            'year': datetime.now().year,
        }
    )

def all_exhibitions(request):
    current_date = timezone.now().date()

    exhibitions = Exhibition.objects.filter(end_date__gte=current_date)
            
    return render(
        request,
        'app/all_exhibitions.html',
        {
            'title': 'Exhibitions',
            'exhibitions': exhibitions,
            'year': datetime.now().year,
        }
    )

@login_required
def purchase_ticket_exhibition(request, id):
    exhibition = Exhibition.objects.get(id=id)

    ticket = Ticket_Exhibition.objects.create(
        visitor=request.user,
        exhibition=exhibition,
        purchase_date=timezone.now(),
        discount_code = None
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

    ticket = Ticket_Excursion.objects.create(
        visitor=request.user,
        excursion=excursion,
        purchase_date=timezone.now(),
        discount_code = None
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

def all_exhibits(request):
    exhibits = Exhibit.objects.all()
    
    return render(
    request,
    'app/all_exhibits.html',
    {
        'title': 'Exhibits',
        'exhibits' : exhibits,
        'year': datetime.now().year,
    }
    )

@login_required
def nationality_by_name(request):
    name = request.user.first_name  
    
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
        
        return render(request, 'app/nationality.html', {'name': name, 'nationalities': result})
    
    except requests.RequestException as e:
        return render(request, 'app/nationality.html', {'error': str(e)})