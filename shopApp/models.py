import datetime

import jdatetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

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


class Size(models.Model):
    name = models.CharField("اندازه", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "اندازه"
        verbose_name_plural = "اندازه‌ها"


class Color(models.Model):
    name = models.CharField("رنگ", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ‌ها"


class Tedad(models.Model):
    name = models.IntegerField("تعداد")  # تغییر به IntegerField

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "تعداد"
        verbose_name_plural = "تعداد"


class Product(models.Model):
    name = models.CharField('نام', max_length=200)
    description = CKEditor5Field('توضیحات', config_name='extends')
    price = models.IntegerField("قیمت")
    picture = models.ImageField("تصویر محصول", upload_to="media/products/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name="دسته‌بندی")#با حذف کتگوری اصلی کل اطلاعات پاک میشود


    size = models.ForeignKey(Size, on_delete=models.SET_NULL,null=True, blank=True, verbose_name="اندازه‌ها")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="رنگ")
    tedad = models.ForeignKey(Tedad, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="تعداد")#با حذف مدل اصلی اطللاعات بقیه پاک نمیشود

    is_sale = models.BooleanField("تخفیف‌دار", default=False)
    sale_price = models.DecimalField("قیمت با تخفیف", max_digits=20, decimal_places=3, default=0)
    star = models.IntegerField("ستاره", default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    quantity = models.IntegerField("تعداد باقی مانده", default=0)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="مشتری")
    quantity = models.IntegerField("تعداد", default=1)
    address = models.CharField("آدرس", max_length=250, default='', blank=False)
    phone = models.CharField("تلفن", max_length=15, help_text="09...", blank=True)
    date_ordered = models.DateTimeField("تاریخ ثبت سفارش", auto_now_add=True)
    timeOrder = models.CharField("زمان سفارش", max_length=50, blank=True, null=True)

    status = models.BooleanField("وضعیت", default=False)
    def save(self, *args, **kwargs):
        if not self.timeOrder:
            self.timeOrder = jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"