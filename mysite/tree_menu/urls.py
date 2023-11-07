from django.urls import path
from tree_menu.views import StartPageView

app_name = 'tree_menu'

urlpatterns = [
    path('tree_menu/', StartPageView.as_view(), name='index')
]
