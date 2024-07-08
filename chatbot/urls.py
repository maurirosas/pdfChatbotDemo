from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('load_pdfs/<str:category>/', views.load_pdfs, name='load_pdfs'),
    path('select_pdf/', views.select_pdf, name='select_pdf'),
]
