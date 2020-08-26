from django.test import Client
from django.contrib.auth.models import User, Permission, ContentType
from wms.models import Location, Zone, Product, Stock,  Cart, OrderList
import pytest
from random import randint


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    models = ContentType.objects.filter(app_label='wms')
    bv = Permission.objects.filter(content_type__in=models)
    user = User.objects.create(username='michal')
    user.set_password('dupadupa')
    user.user_permissions.set(bv)
    user.save()
    return user


@pytest.fixture
def zones():
    items = []
    for x in ['fghijhj']:
        t = Zone.objects.create(zone=x)
        items.append(t)
    return items


@pytest.fixture
def locations(zones):
    items = []
    c = randint(10,99)
    for zone in zones:
        t = Location.objects.create(zone=zone, location=f'{c}.{c}.{c}')
        items.append(t)
    return items


@pytest.fixture
def products():
    items = []
    z = randint(100000, 999999)
    for x in ['pjpopj']:
        t = Product.objects.create(name=x, code=z, description=x, price='0.99', date_to_use='2020-10-10')
        items.append(t)
    return items


@pytest.fixture
def stock(products, locations):
    items = []
    for product in products:
        for location in locations:
            r = Stock.objects.create(product=product, localization=location, stock='100')
            items.append(r)
    return items


@pytest.fixture
def carts(products, user):

    t = Cart.objects.create(user=user)
    for product in products:
        OrderList.objects.create(cart=t, product=product, amount=1)
    return t


@pytest.fixture
def orderlists(carts, products):
    items = []
    for product in products:
        t = OrderList.objects.create(product=product, cart=carts, amount=1)
        items.append(t)
    return items