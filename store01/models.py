from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


# Create your models here.
class category01(models.Model):
    name=models.CharField(max_length=255,unique=True,verbose_name = "ชื่อประเภทสินค้า")
    slug=models.SlugField(max_length=255,unique=True,verbose_name = "ชื่อประเภทสินค้าภาษาอังกฤษ")

    def __str__(self):
        return self.name

    class Meta :
        ordering=('name',)
        verbose_name='ประเภทสินค้า'
        verbose_name_plural='ข้อมูลประเภทสินค้า'

    def get_url(self):
        return reverse('product_by_category',args=[self.slug])

class product01(models.Model):
    name=models.CharField(max_length=255,unique=True,verbose_name = "ชื่อสินค้า")
    slug=models.SlugField(max_length=255,unique=True,null=False,verbose_name = "ชื่อสินค้าภาษาอังกฤษ")
    description=models.TextField(blank=True,verbose_name = "รายละเอียดสินค้า")
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name = "ราคา")
    image=models.ImageField(upload_to="MEDIA/",blank=True,verbose_name = "ภาพสินค้า")
    stock=models.IntegerField(verbose_name = "จำนวนสินค้าที่พร้อมขาย")
    unit=models.CharField(max_length=255,blank=True,verbose_name = "หน่วยของสินค้า(ถุง/กล่อง/ชิ้น/ฯลฯ)")
    available=models.BooleanField(default=True,verbose_name = "สินค้าพร้อมขายหรือไม่")
    created=models.DateTimeField(auto_now_add=True,verbose_name = "วันที่สร้างข้อมูลสินค้า")
    updated=models.DateTimeField(auto_now=True,verbose_name = "วันที่แก้ไขข้อมูลสินค้า")
    category=models.ForeignKey(category01,on_delete=models.CASCADE,verbose_name = "ประเภทสินค้า")

    def __str__(self):
         return self.name
    
    def admin_image(self):
       return mark_safe('<img src="{}" width="100" />'.format(self.image.url))
        
    # admin_image.short_description = 'Image'
    # admin_image.allow_tags = True

    class Meta :
        ordering=('name',)
        verbose_name='สินค้า'
        verbose_name_plural='ข้อมูลสินค้า'
        # verbose_unit='หน่วย(ถุง/ชิ้น/ลูก)'

    def get_url(self):
        return reverse('productDetail',args=[self.category.slug,self.slug])

class Cart(models.Model):
    cart_id=models.CharField(max_length=255,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
    class Meta:
        db_table='cart'
        ordering=('date_added',)
        verbose_name='ตะกร้าสินค้า'
        verbose_name_plural="ข้อมูลตะกร้าสินค้า"

class CartItem(models.Model):
    product=models.ForeignKey(product01,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    active=models.BooleanField(default=True)

    class Meta:
        db_table='cartItem'
        verbose_name='รายการสินค้าในตะกร้า'
        verbose_name_plural="ข้อมูลรายการสินค้าในตะกร้า"
    
    def sub_total(self):
        return self.product.price * self.quantity 
    
    def __str__(self):
        return self.product.name

class Order(models.Model):
    name=models.CharField(max_length=255,blank=True,verbose_name = "ชื่อลูกค้า")
    address=models.CharField(max_length=255,blank=True,verbose_name = "บ้านเลขที่ที่อยู่จัดส่ง")
    city=models.CharField(max_length=255,blank=True,verbose_name = "ที่อยู่จัดส่ง")
    postcode=models.CharField(max_length=255,blank=True,verbose_name = "รหัสไปรษณีย์")
    total=models.DecimalField(max_digits=10,decimal_places=2,verbose_name = "ราคาสินค้าทั้งหมด")
    email=models.EmailField(max_length=250,blank=True,verbose_name = "อีเมลลูกค้า")
    token=models.CharField(max_length=255,blank=True)
    created=models.DateTimeField(auto_now_add=True,verbose_name = "วันที่ได้รับคำสั่งซื้อ")
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='Order'
        ordering=('id',)
        verbose_name='ข้อมูลใบสั่งซื้อ'
        verbose_name_plural="ข้อมูลใบสั่งซื้อ"
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product=models.CharField(max_length=250,verbose_name = "สินค้า")
    quantity=models.IntegerField(verbose_name = "จำนวน")
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name = "ราคาต่อชิ้น")
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name = "คำสั่งซื้อ")
    created=models.DateTimeField(auto_now_add=True,verbose_name = "วันที่ได้รับคำสั่งซื้อ")
    updated=models.DateTimeField(auto_now=True)
    image = product01()


    class Meta :
        db_table='OrderItem'
        ordering=('order',)
        verbose_name='รายการสินค้าในใบสั่งซื้อ'
        verbose_name_plural="ข้อมูลสินค้าในใบสั่งซื้อ"

    def sub_total(self):
        return self.quantity*self.price
    
    def __str__(self):
        return self.product

class BankTransfer(models.Model):
    name = models.CharField(max_length=255,verbose_name = "ชื่อลูกค้า")
    address = models.CharField(max_length=255,verbose_name = "บ้านเลขที่ที่อยู่จัดส่ง")
    city = models.CharField(max_length=255,verbose_name = "ที่อยู่จัดส่ง")
    postcode = models.CharField(max_length=10,verbose_name = "รหัสไปรษณีย์")
    email = models.EmailField(verbose_name = "อีเมลลูกค้า")
    money_transfer_slip = models.ImageField(upload_to='bank_transfer_slips/',verbose_name = "สลิปโอนเงิน",)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name = "คำสั่งซื้อ")
    
    def admin_image(self):
        return mark_safe('<img src="{}" width="225" />'.format(self.money_transfer_slip.url)) 

    class Meta :
        verbose_name='ใบสั่งซื้อพร้อมสลิปโอนเงิน'
        verbose_name_plural="ใบสั่งซื้อพร้อมสลิปโอนเงิน"

    
