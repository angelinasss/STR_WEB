from django.contrib import admin
from .models import Article, Banner, CompanyInfo, FAQ, Job, Partners, Review, PromoCode, PrivacyPolicy, ArtType, Hall, Position, Employee, Exhibit, Exhibition, Excursion, Ticket_Excursion, Ticket_Exhibition

admin.site.register(PrivacyPolicy)
admin.site.register(ArtType)
admin.site.register(Exhibit)
admin.site.register(Exhibition)
admin.site.register(Excursion)
admin.site.register(Ticket_Excursion)
admin.site.register(Ticket_Exhibition)
admin.site.register(Banner)
admin.site.register(Partners)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
     list_display = ('user', 'rating', 'text', 'created_at')
     list_filter = ('rating', 'created_at')
     
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
     list_display = ('title', 'content', 'short_description', 'published_at')
     
@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
     list_display = ('description', 'history', 'details')
     
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
     list_display = ('question', 'answer', 'added_date')
     
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
     list_display = ('title', 'description', 'requirements', 'salary')
     
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
     list_display = ('code', 'discount', 'expiration_date', 'is_active')
     fieldsets = (
        (None, {
            'fields': ('code','discount')
        }),
        ('Availability', {
            'fields': ('expiration_date', 'is_active')
        }),
     )
     
class EmployeeInline(admin.TabularInline):
    model = Employee
     
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
     list_display = ('name', 'number', 'floor', 'area')
     list_filter = ('floor', 'area')
     fields = ['name', 'area', ('number', 'floor')]
     inlines = [EmployeeInline]
     
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
     inlines = [EmployeeInline]
     
     
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
     list_display = ('first_name', 'last_name', 'phone', 'position', 'hall', 'email')

