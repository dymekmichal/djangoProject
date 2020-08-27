import datetime

from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


def length_validation(value):
    """
    Funkcja używana jako walidacja ilości wpisanych w formularzu znaków.
    """
    if len(value) != 6:
        raise ValidationError("Kod produktu musi się składać z 6 cyfr!")


def date_validation(value):
    """
        Funkcja używana jako walidacja daty ustawionej w formularzu, zwracająca błąd
        w przypadku wpisania daty wcześniejszej niż obecny dzień.
    """
    if value < datetime.date.today():
        raise ValidationError("Produkt już jest przeterminowany!")


class Location(models.Model):
     """
        Model, w którym tworzy się dokładną lokalizację produktu, znajdującego się w określonej strefie.
    """
    location = models.CharField(max_length=8, verbose_name="Lokalizacja (xx.xx.xx):", unique=True, primary_key=False)
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE, verbose_name="Strefa:")

    def get_detail_url(self):
        return f"/wms/locations/{self.pk}"

    def get_delete_url(self):
        return reverse('delete_location', args=(self.pk,))

    def __str__(self):
        return f'{self.location} - {self.zone}'


class Zone(models.Model):
    """
        Model tworzenia stref przechowywania w obiekcie magazynowym.
    """
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
     """
        Model tworzenia produktu jako obiektu, który nie ma jeszcze określonej ilości i nie ma przypisanego miejsca składowania.
    """
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
    """
        Model, w którym dla danego produktu określana jest jego ilość w wybranej, stworzonej wcześniej lokalizacji.
    """
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
     """
        Model koszyka, w którym przechowywane są wybrane przez użytkownika produkty oraz określana jest metoda ich dostarczenia do użytkownika.
    """
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
    """
        Model listy zamówień, w którym określamy jaką ilość danego produktu chcemy zamówić i przechować w koszyku.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt:")
    amount = models.IntegerField(verbose_name="Ilość")

    def get_detail_url(self):
        return f"/wms/orders/{self.pk}"

    def get_delete_url(self):
        return reverse('delete_order', args=(self.pk,))

    def __str__(self):
        return f'{self.product} w ilości {self.amount}'
