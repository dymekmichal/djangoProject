from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from wms.models import Location, Zone, Product, Stock, OrderList, Cart


class DateInput(forms.DateInput):
    input_type = 'date'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {"date_to_use": DateInput()}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "user_permissions"]
        widgets = {
            'user_permissions': forms.CheckboxSelectMultiple()
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = "__all__"


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        exclude = ('product','user')
        # widgets = {
        #     'delivery': forms.Select()
        # }


class OrderListForm(forms.ModelForm):
    class Meta:
        model = OrderList
        fields = ['product', 'amount']


    def clean(self):
        clean_data = super().clean()
        amount = clean_data['amount']
        product = clean_data['product']
        stock = Stock.objects.get(product=product)
        if amount > stock.stock:
            raise ValidationError("Brak takiej ilości na stanie")
        stock.stock -= amount
        stock.save()
