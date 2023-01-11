import imp
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path
from store01 import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="home"),
    path('category/<slug:category_slug>',views.index,name="product_by_category"),
    path('product/<slug:category_slug>/<slug:product_slug>',views.productPage,name='productDetail'),
    path('cart/add/<int:product_id>',views.addCart,name="addCart"),
    path('cartdetail/',views.cartdetail,name="cartdetail"),
    path('cart/remove/<int:product_id>',views.removeCart,name="removeCart"),
    path('cart/remove2/<int:product_id>',views.removefullCart,name="removefullCart"),
    path('account/create',views.signUpView,name="signUp"),
    path('account/profile',views.profile,name="profile"),
    path('account/login',views.signInView,name="signIn"),
    path('account/logout',views.signOutView,name="signOut"),
    path('search/',views.search,name='search'),
    path('orderHistory/',views.orderHistory,name="orderHistory"),
    path('order/<int:order_id>',views.viewOrder,name="orderDetails"),
    path('cart/thankyou',views.thankyou,name='thankyou'),
    path('account/Editprofile',views.Editprofile,name="Edit"),
    path('account/success',views.success,name='success'),
    path('passwordwrong',views.passwrong,name='passwrong'),
    path('password/',views.change_password,name="password"),
    path('show/',views.show,name="show"),
    path('payment/', views.process_payment, name='process_payment')

]

if settings.DEBUG :
    # /media/product/
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    # /static/
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
# /static/media/product/
