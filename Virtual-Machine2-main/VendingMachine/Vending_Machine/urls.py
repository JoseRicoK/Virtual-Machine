from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pagar/', views.pagar, name='pagar'),
    path('zonaAdmin/', views.zonaAdmin, name='zonaAdmin'),
    path('zonaAdmin/lista-productos/', views.ProductListView.as_view(), name='producto-list'),
    path('zonaAdmin/lista-productos/<int:pk>', views.ProductDetailView.as_view(), name='producto-detail'),
    path('zonaAdmin/lista-productos/<int:pk>/edit', views.ProductEditView.as_view(), name='producto-edit'),
    path('zonaAdmin/alertar-proveedor/', views.alertarProveedor, name='alertar-proveedor'),
    path('zonaAdmin/ver-estadisticas', views.verEstadisticas, name='ver-estadisticas')
]