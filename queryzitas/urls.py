from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    HomePageView,
    InsertFormView,
    DeleteFormView,
    ReadFormView,
    FaturamentoFormView
)

app_name='queryzitas'

urlpatterns = [
    #home
    path('', HomePageView.as_view(), name='home'),
    #procedures
    path('insert/', InsertFormView.as_view(), name='insert'),
    path('delete/', DeleteFormView.as_view(), name='delete'),
    path('read/', ReadFormView.as_view(), name='read'),
    #function
    path('faturamento/', FaturamentoFormView.as_view(), name='faturamento'),
]