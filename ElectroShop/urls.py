from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # App-level routes
    path('api/users/', include('Users.urls')),
    path('api/products/', include('Products.urls')),
    path('api/orders/', include('Orders.urls')),
    path('api/payments/', include('Payments.urls')),
    path('api/shipping/', include('Shipping.urls')),
    path('api/cart/', include('Cart.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
