"""
Definition of urls for MuseumWebApp.
"""

from datetime import datetime
from django.urls import re_path
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^news/$', views.news, name='news'),
    re_path(r'^faq/$', views.faq, name='faq'),
    re_path(r'^faq/create_FAQ/$', views.create_FAQ, name='create_faq'),
    re_path(r'^faq/edit_FAQ/(?P<id>\d+)/$', views.edit_FAQ, name='edit_faq'),
    re_path(r'^faq/delete_FAQ/(?P<id>\d+)/$', views.delete_FAQ, name='delete_faq'),
    re_path(r'^contact/$', views.contact, name='contact'),
     re_path(r'^employee_list/$', views.employee_list, name='employee_list'),
    re_path(r'^contact/contact_create/$', views.contact_create, name='contact_create'),
    re_path(r'^contact/contact_delete/(?P<id>\d+)/$', views.contact_delete, name='contact_delete'),
    re_path(r'^vacancies/$', views.vacancies, name='vacancies'),
    re_path(r'^reviews/$', views.reviews, name='reviews'),
    re_path(r'^reviews/create_review/$', views.create_review, name='create_review'),
    re_path(r'^reviews/edit_review/(?P<id>\d+)/$', views.edit_review, name='edit_review'),
    re_path(r'^reviews/delete_review/(?P<id>\d+)/$', views.delete_review, name='delete_review'),
    re_path(r'^profile/(?P<id>\d+)/$', views.profile, name='profile'),
    re_path(r'^privacy-policy/$', views.privacy_policy, name='privacy_policy'),
    re_path(r'^promo_codes/$', views.promo_codes, name='promo_codes'),
    re_path(r'^promo_codes/create_promo_code/$', views.create_promo_code, name='create_promo_code'),
    re_path(r'^promo_codes/edit_promo_code/(?P<id>\d+)/$', views.edit_promo_code, name='edit_promo_code'),
    re_path(r'^promo_codes/delete_promo_code/(?P<id>\d+)/$', views.delete_promo_code, name='delete_promo_code'),
    re_path(r'^news/create_article/$', views.create_article, name='create_article'),
    re_path(r'^news/editArticle/(?P<id>\d+)/$', views.editArticle, name='edit_article'),
    re_path(r'^news/deleteArticle/(?P<id>\d+)/$', views.deleteArticle, name='delete_article'),
    re_path(r'^news/article_detail/(?P<id>\d+)/$', views.article_detail, name='article_detail'),
    re_path(r'^vacancies/create_job/$', views.create_job, name='create_job'),
    re_path(r'^vacancies/edit_job/(?P<id>\d+)/$', views.edit_job, name='edit_job'),
    re_path(r'^vacancies/delete_job/(?P<id>\d+)/$', views.delete_job, name='delete_job'),
    re_path(r'^about/edit_company_info/$', views.edit_company_info, name='edit_company_info'),
    re_path(r'^login/register/$', views.register, name='register'),
    re_path(r'^hall_info/$', views.hall_info, name='hall_info'),
    re_path(r'^newest_exhibits/$', views.newest_exhibits, name='newest_exhibits'),
    re_path(r'^employees_by_floor/$', views.employees_by_floor, name='employees_by_floor'),
    re_path(r'^exhibits_by_arrival_date/$', views.exhibits_by_arrival_date, name='exhibits_by_arrival_date'),
    re_path(r'^excursions_by_season/$', views.excursions_by_season, name='excursions_by_season'),
    re_path(r'^my_exhibits/$', views.my_exhibits, name='my_exhibits'),
    re_path(r'^my_excursions/$', views.my_excursions, name='my_excursions'),
    re_path(r'^all_excursions/$', views.all_excursions, name='all_excursions'),
    re_path(r'^my_tickets/$', views.my_tickets, name='my_tickets'),
    re_path(r'^all_exhibits/$', views.all_exhibits, name='all_exhibits'),
    re_path(r'^nationality/$', views.nationality_by_name, name='nationality_by_name'),
    re_path(r'^all_excursions/purchase_ticket_excursion/(?P<id>\d+)/$', views.purchase_ticket_excursion, name='purchase_ticket_excursion'),
    re_path(r'^all_exhibitions/$', views.all_exhibitions, name='all_exhibitions'),
    re_path(r'^all_exhibitions/purchase_ticket_exhibition/(?P<id>\d+)/$', views.purchase_ticket_exhibition, name='purchase_ticket_exhibition'),
    re_path(r'^excursions_by_season/excursion_delete/(?P<id>\d+)/$', views.excursion_delete, name='excursion_delete'),
    re_path(r'^excursions_by_season/excursion_edit/(?P<id>\d+)/$', views.excursion_edit, name='excursion_edit'),
    re_path(r'^create_excursion/$', views.create_excursion, name='create_excursion'),
    re_path(r'^newest_exhibits/create_new_exhibit/$', views.create_new_exhibit, name='create_new_exhibit'),
    re_path(r'^hall_detail/(?P<id>\d+)/$', views.hall_detail, name='hall_detail'),
    re_path(r'^hall_info/edit_hall/(?P<id>\d+)/$', views.edit_hall, name='edit_hall'),
    re_path(r'^hall_info/create_hall/$', views.create_hall, name='create_hall'),
    re_path(r'^hall_info/delete_hall/(?P<id>\d+)/$', views.delete_hall, name='delete_hall'),
    re_path(r'^hall_detail/(?P<id>\d+)/create_exhibit/$', views.create_exhibit, name='create_exhibit'),
    re_path(r'^hall_detail/(?P<id>\d+)/edit_exhibit/$', views.edit_exhibit, name='edit_exhibit'),
    re_path(r'^hall_detail/(?P<id>\d+)/delete_exhibit/$', views.delete_exhibit, name='delete_exhibit'),
    re_path(r'^statistics/$', views.statistics, name='statistics'),
    re_path(
        r'^login/$',
        LoginView.as_view(
            template_name='app/login.html',
            authentication_form=forms.BootstrapAuthenticationForm,
            extra_context={
                'title': 'Log in',
                'year': datetime.now().year,
            }
        ),
        name='login'
    ),
    re_path(r'^logout/$', LogoutView.as_view(next_page='/'), name='logout'),
    re_path(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
