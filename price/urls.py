from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'price'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('add/', views.PersonCreateView.as_view(), name='add'),
    path ('<int:pk>/', views.DetailView.as_view (), name='detail'),
    path('search/', views.search_item, name='search_item_view'),

    # /price/2/update
    path('update/<int:pk>', views.ItemUpdate.as_view(), name='item_update'),

    # /price/2/delete
    path ('<int:pk>/delete', views.ItemDelete.as_view(), name='item_delete'),

    url (r'^import/', views.import_data, name="import"),
]