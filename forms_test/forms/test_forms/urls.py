from django.urls import path,include

# Пакет приложения
from test_forms.views import *

urlpatterns = [
    path('get_form/',form),
    path('test/',test),
    #path('thanks/',thanks_page, name = "thanks_page")
]
