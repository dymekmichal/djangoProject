from django.urls import path
from wms import views

urlpatterns = [
    path('', views.index, name='index'),
    path("products/", views.ProductView.as_view(), name='products'),
    path("products/<int:pk>", views.ProductView.as_view(), name='product'),
    path("products/delete/<int:pk>", views.ProductDeleteView.as_view(), name='delete_product'),
    path("locations/", views.LocationView.as_view(), name='locations'),
    path("locations/<int:pk>", views.LocationView.as_view(), name='location'),
    path("locations/delete/<int:pk>", views.LocationDeleteView.as_view(), name='delete_location'),
    path("zones/", views.ZoneView.as_view(), name='zones'),
    path("zone/<int:pk>", views.ZoneView.as_view(), name='zone'),
    path("zones/delete/<int:pk>", views.ZoneDeleteView.as_view(), name='delete_zone'),
    path("stocks/", views.StockView.as_view(), name='stocks'),
    path("stocks/<int:pk>", views.StockView.as_view(), name='stock'),
    path("stocks/delete/<int:pk>", views.StockDeleteView.as_view(), name='delete_stock'),
    path("orders/", views.OrderListView.as_view(), name='orders'),
    path("orders/<int:pk>", views.OrderListView.as_view(), name='order'),
    path("orders/delete/<int:pk>", views.OrderListDeleteView.as_view(), name='delete_order'),
    path("carts/", views.DetailCartView.as_view(), name='carts'),
    # path('products/search/', views.SearchProductView.as_view()), na przyszłość, wprowadzić wyszukiwanie produktór

]
