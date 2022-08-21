from django.urls import path
from .views import (
    ProductListView, ProductDetail,
    FilesView, FileDetailView,
    CategoryView, CategoryDetailView,
)

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListView.as_view(), name='products-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<int:product_id>/files/', FilesView.as_view(), name='file-view'),
    path('products/<int:product_id>/files/<int:pk>/', FileDetailView.as_view(), name='file-detail'),
]

