from audioop import reverse
from itertools import product
from django.shortcuts import render,get_object_or_404,redirect
from store01.models import product01,category01,Cart,CartItem,Order,OrderItem,BankTransfer
from store01.forms import SignUpForm,UserEdit,PasswordChangeForm,BankTransferForm
from django.contrib import messages
from django.contrib.auth.models import Group,User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.conf import settings
from django.core.exceptions import ValidationError
import stripe
from django.core.files.storage import default_storage



def show(request):
    if request.user.is_staff:
        showdata=Order.objects.all()
    return render(request,'show.html',{"data":showdata})

def index(request,category_slug=None):
    product02=None
    categories=None
    if category_slug!=None:
        categories=get_object_or_404(category01,slug=category_slug)
        product02=product01.objects.all().filter(category=categories,available=True)
    else :
        product02=product01.objects.all().filter(available=True)

    paginator=Paginator(product02,3)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        productperPage=paginator.page(page)
    except (EmptyPage,InvalidPage):
        productperPage=paginator.page(paginator.num_pages)

    return render(request,'index.html',{'product04':productperPage,'category':categories})

def productPage(request,category_slug,product_slug):
    try:
        product03=product01.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e :
          raise e
    return render(request,'product09.html',{'product':product03})
    
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
@login_required(login_url='signIn')

def cartdetail(request):
    total=0
    counter=0
    cart_items=None
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) 
        cart_items=CartItem.objects.filter(cart=cart,active=True) 
        for item in cart_items:
            total+=(item.product.price*item.quantity)
            counter+=item.quantity
    except Exception as e :
        pass

    stripe.api_key=settings.SECRET_KEY
    stripe_total=int(total*100)+5000
    description="ชำระแบบออนไลน์"
    data_key=settings.PUBLIC_KEY

    if request.method=="POST":
        
        try :
            token=request.POST['stripeToken']
            email=request.POST['stripeEmail']
            name=request.POST['stripeBillingName']
            address=request.POST['stripeBillingAddressLine1']
            city=request.POST['stripeBillingAddressCity']
            postcode=request.POST['stripeShippingAddressZip']

            customer=stripe.Customer.create(
                email=email,
                source=token
            )
            charge=stripe.Charge.create(
                amount=stripe_total,
                currency='thb',
                description=description,
                customer=customer.id
            )

            order=Order.objects.create(
                name=name,
                address=address,
                city=city,
                postcode=postcode,
                total=total+50,
                email=email,
                token=token
            )
            order.save()

            # #บันทึกรายการสั่งซื้อ
            for item in cart_items :
                order_item=OrderItem.objects.create(
                    product=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price,
                    order=order
                )
                order_item.save()
                #ลดจำนวน Stock
                product=product01.objects.get(id=item.product.id)
                product.stock=int(item.product.stock-order_item.quantity)
                product.save()
                item.delete()
            return redirect('thankyou')
            

        except stripe.error.CardError as e :
            return False , e

    return render(request,'cartdetail.html',
    dict(cart_items=cart_items,total=total,counter=counter,data_key=data_key,stripe_total=stripe_total,description=description))


def process_payment(request):
    form=BankTransferForm(request.POST, request.FILES)
    total = 0
    counter=0
    cart_items = None
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for item in cart_items:
            total += (item.product.price * item.quantity)
        shipping = 50
    except Exception as e:
        pass

    if request.method == "POST":
        total_cost = total + shipping
        context = {
            'total_cost': total_cost,
            # other context variables
        }
        
        try :
            money_transfer_slip = request.POST.get('สลิปโอนเงิน') 
            token = request.POST.get('', '')
            email = request.POST.get('อีเมลลูกค้า', '')
            name = request.POST.get('ชื่อลูกค้า', '')
            address = request.POST.get('บ้านเลขที่ที่อยู่จัดส่ง', '')
            city = request.POST.get('ที่อยู่จัดส่ง', '')
            postcode = request.POST.get('รหัสไปรษณีย์', '')
            shipping = 50
            
            order=Order.objects.create(
                name=name,
                address=address,
                city=city,
                postcode=postcode,
                total=total+shipping,
                email=email,
                token=token
            )
            order.save()

            banktransfer = BankTransfer.objects.create(
            money_transfer_slip=request.FILES['money_transfer_slip'],
            name=name,
            address=address,
            city=city,
            postcode=postcode,
            email=email,
            order=order
            )
            banktransfer.save()


            # #บันทึกรายการสั่งซื้อ
            for item in cart_items :
                order_item=OrderItem.objects.create(
                    product=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price,
                    order=order
                )
                order_item.save()
                #ลดจำนวน Stock
                product=product01.objects.get(id=item.product.id)
                product.stock=int(item.product.stock-order_item.quantity)
                product.save()
                item.delete()
            return redirect('thankyou')

        except stripe.error.CardError as e :
            return False , e

    return render(request,'cartdetail.html',context,)


def removeCart(request,product_id):
        cart=Cart.objects.get(cart_id=_cart_id(request))
        product=get_object_or_404(product01,id=product_id)
        cartItem=CartItem.objects.get(product=product,cart=cart)
        cartItem.quantity-=1
        cartItem.save()
        return redirect('cartdetail')

def removefullCart(request,product_id):
        cart=Cart.objects.get(cart_id=_cart_id(request))
        product=get_object_or_404(product01,id=product_id)
        cartItem=CartItem.objects.get(product=product,cart=cart)
        cartItem.delete()
        return redirect('cartdetail')

def addCart(request,product_id):
    product=product01.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        #ซื้อรายการสินค้าซ้ำ
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity<cart_item.product.stock :
            #เปลี่ยนจำนวนรายการสินค้า
            cart_item.quantity+=1
            #บันทึก/อัพเดทค่า
            cart_item.save()
    except CartItem.DoesNotExist:
        #ซื้อรายการสินค้าครั้งแรก
        #บันทึกลงฐานข้อมูล
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    return redirect('cartdetail')






def signUpView(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            signUpUser=User.objects.get(username=username)
            customer_group=Group.objects.get(name="Customer")
            customer_group.user_set.add(signUpUser)
            return redirect('success')
    else :
        form=SignUpForm()
    return render(request,"signup.html",{'form':form})

def signInView(request):
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None :
                login(request,user)
                return redirect('home')
            else :
                return redirect('signUp')
    else:
        form=AuthenticationForm()
    return render(request,'signIn.html',{'form':form})

def signOutView(request):
    logout(request)
    return redirect('signIn')

def profile(request):
    return render(request,'profile.html')

def search(request):
    productSearch=product01.objects.filter(name__contains=request.GET['title'])
    return render(request,'index.html',{'product04':productSearch})

def orderHistory(request):
    if request.user.is_authenticated:
        email=str(request.user.email)
        orders=Order.objects.filter(email=email)
    return render(request,'orders.html',{'orders':orders})

def viewOrder(request,order_id):
    if request.user.is_authenticated:
        email=str(request.user.email)
        order=Order.objects.get(email=email,id=order_id)
        orderitem=OrderItem.objects.filter(order=order)
    return render(request,'viewOrder.html',{'order': order, 'order_items': orderitem})

def thankyou(request):
    return render(request,'thankyou.html')

def success(request):
    return render(request,'success.html')

def passwrong(request):
    return render(request,'PassX.html')

def Editprofile(request):
    if request.method == 'POST':
        form = UserEdit(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('success')
            # return redirect(reverse('account/profile'))
    else:
        form = UserEdit(instance=request.user)
        args = {'form': form}
        return render(request, 'Editprofile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('success')
        else:
            return redirect('passwrong')
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'password.html', args)
