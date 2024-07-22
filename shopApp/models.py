import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField("نام",max_length=25)

    def __str__(self):  # باعث میشه نام در پنل ادمین نمایش داده بشه
        return self.name
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Customer(models.Model):
    first_name = models.CharField("نام",max_length=15)
    last_name = models.CharField("نام خانوادگی",max_length=25)
    email = models.EmailField("ایمیل")
    phone = models.CharField("تلفن",max_length=15, help_text="09...")
    password = models.CharField("رمز عبور",max_length=30)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتری ها"


class Product(models.Model):
    name = models.CharField("نام", max_length=250)
    description = models.TextField("توضیحات", blank=True, default='')
    price = models.IntegerField("قیمت")
    picture = models.ImageField("تصویر محصول", upload_to="media/products/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name="دسته‌بندی")
    sizes = (
        ('S', '32'),
        ('M', '42'),
        ('L', '48'),
        ('XL', '52'),
    )
    size = models.CharField("اندازه", max_length=10, choices=sizes, default='M')
    is_sale = models.BooleanField("تخفیف‌دار", default=False)
    sale_price = models.DecimalField("قیمت با تخفیف", max_digits=20, decimal_places=3, default=0)
    star = models.IntegerField("ستاره", default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name="محصول")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,verbose_name="مشتری")
    quantity = models.IntegerField("تعداد",default=1)
    address = models.CharField("آدرس",max_length=250, default='', blank=False)
    phone = models.CharField("تلفن",max_length=15, help_text="09...", blank=True)
    date_ordered = models.DateTimeField("تاریخ ثبت سفارش",auto_now_add=True)
    status = models.BooleanField("وضعیت",default=False)

    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"