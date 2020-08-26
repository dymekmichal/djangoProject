import datetime

from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


def length_validation(value):
    if len(value) != 6:
        raise ValidationError("Kod produktu musi się składać z 6 cyfr!")


def date_validation(value):
    if value < datetime.date.today():
        raise ValidationError("Produkt już jest przeterminowany!")


class Location(models.Model):
    location = models.CharField(max_length=8, verbose_name="Lokalizacja (xx.xx.xx):", unique=True, primary_key=False)
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE, verbose_name="Strefa:")

    def get_detail_url(self):
        return f"/wms/locations/{self.pk}"

    def get_delete_url(self):
        return reverse('delete_location', args=(self.pk,))

    def __str__(self):
        return f'{self.location} - {self.zone}'


class Zone(models.Model):
    zone = models.CharField(max_length=16, verbose_name="Strefa: ")

    def get_detail_url(self):
        return f"/wms/zone/{self.pk}"

    def get_delete_url(self):
        return reverse('delete_zone', args=(self.pk,))

    def get_locations(self):
        return self.location_set.all()

    def __str__(self):
        return self.zone


class Product(models.Model):
    name = models.CharField(max_length=32, verbose_name="Nazwa produktu:")
    code = models.CharField(max_length=6, unique=True, primary_key=False, validators=[length_validation],
                            verbose_name="Kod produktu (6 cyfr):")
    description = models.CharField(max_length=64, null=True, verbose_name="Opis produktu:")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Cena jednostkowa [PLN]:")
    date_to_use = models.DateField(null=True, verbose_name="Data przydatności:", validators=[date_validation])

    def get_detail_url(self):
        return f"/wms/products/{self.pk}"

    def get_delete_url(self):
        return reverse('delete_product', args=(self.pk,))

    def __str__(self):
        return f'{self.name}, Kod systemowy produktu: {self.code}, BBD: {self.date_to_use}'


class Stock(models.Model):
    product = models.ForeignKey(Product, verbose_name="Produkt:", on_delete=models.CASCADE)
    localization = models.ForeignKey(Location, verbose_name="Lokalizacja:", on_delete=models.CASCADE)
    stock = models.IntegerField(verbose_name="Ilość:")

    def get_detail_url(self):
        return f"/wms/stocks/{self.pk}"

    def get_delete_url(self):
        return reverse('delete_stock', args=(self.pk,))

    def __str__(self):
        return f"{self.product.name}, dostępna ilość: {self.stock}"


class Cart(models.Model):
    DELIVERY_CHOICE = (
        ("Transport z magazynu", "Transport z magazynu"),
        ("Odbiór własny", "Odbiór własny"),
        ("Kurier", "Kurier"),
        ("FoodPost", "FoodPost"),
        ("Poprzez przedstawiciela", "Poprzez przedstawiciela")
    )
    delivery = models.CharField(choices=DELIVERY_CHOICE, max_length=32, verbose_name="Sposób dostawy:")
    product = models.ManyToManyField(Product, through="OrderList")
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class OrderList(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt:")
    amount = models.IntegerField(verbose_name="Ilość")

    def get_detail_url(self):
        return f"/wms/orders/{self.pk}"

    def get_delete_url(self):
        return reverse('delete_order', args=(self.pk,))

    def __str__(self):
        return f'{self.product} w ilości {self.amount}'
