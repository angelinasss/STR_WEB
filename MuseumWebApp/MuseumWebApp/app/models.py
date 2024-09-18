from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    short_description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    alt_text = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.alt_text or "Without description"
    
class Partners(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField()

    def __str__(self):
        return self.name

class CompanyInfo(models.Model):
    description = models.TextField()
    logo = models.ImageField(upload_to='company_logo/', blank=True, null=True)
    video = models.FileField(upload_to='company_videos/', blank=True, null=True)
    history = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)  
    banners = models.ManyToManyField(Banner, blank=True)  

    def __str__(self):
        return "Company Info"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question
    
class PrivacyPolicy(models.Model):
    content = models.TextField()

    def __str__(self):
        return "Privacy Policy"
    
class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username}'

class PromoCode(models.Model):
    code = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class ArtType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Hall(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    floor = models.IntegerField()
    area = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (Floor {self.floor})"
    
class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=15)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='contact/', blank=True, null=True)
    email = models.EmailField(null=True, blank=True) 

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Exhibit(models.Model):
    name = models.CharField(max_length=200)
    art_type = models.ForeignKey(ArtType, on_delete=models.CASCADE)
    date_acquired = models.DateField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    caretaker = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Exhibition(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    exhibits = models.ManyToManyField(Exhibit)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Excursion(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    date = models.DateField()
    season = models.CharField(max_length=10, choices=[('summer', 'Summer'), ('autumn', 'Autumn'), ('winter', 'Winter'), ('spring', 'Spring')])
    group_size = models.IntegerField()
    guide = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_object.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.content_object.price * self.quantity
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_cost(self):
        return sum(item.total_price for item in self.items.all())
    
class Ticket_Excursion(models.Model):
    visitor = models.ForeignKey(User, on_delete=models.CASCADE)
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Ticket for {self.excursion.name} by {self.visitor.username}"
    
class Ticket_Exhibition(models.Model):
    visitor = models.ForeignKey(User, on_delete=models.CASCADE)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Ticket for {self.exhibition.name} by {self.visitor.username}"