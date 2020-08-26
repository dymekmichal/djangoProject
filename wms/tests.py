from django.urls import reverse
import pytest


def test_base_view(client):
    response = client.get('/')
    assert response.status_code == 200



@pytest.mark.django_db
def test_product_delete_view(client, user):
    client.login(username = 'michal', password='dupadupa')
    response = client.get(reverse('products'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_location_delete_view(client, user):
    client.login(username = 'michal', password='dupadupa')
    response = client.get(reverse('locations'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_zone_delete_view(client, user):
    client.login(username = 'michal', password='dupadupa')
    response = client.get(reverse('zones'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_delete_view(client, user):
    client.login(username = 'michal', password='dupadupa')
    response = client.get(reverse('stocks'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_orderlist_delete_view(client, user):
    client.login(username = 'michal', password='dupadupa')
    response = client.get(reverse('orders'))
    assert response.status_code == 200


########################################################################################################################

@pytest.mark.django_db
def test_product_view(client, user):
    client.login(username = 'michal', password='dupadupa')
    response = client.get(reverse('products'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_location_view(client, user):
    client.login(username = 'michal', password='dupadupa')
    response = client.get(reverse('locations'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_zones_view(client, user):
    client.login(username = 'michal', password='dupadupa')
    response = client.get(reverse('zones'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_stocks_view(client, user):
    client.login(username = 'michal', password='dupadupa')
    response = client.get(reverse('stocks'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_createcarts_view(client, user):
    response = client.get(reverse('carts'))
    assert response.status_code == 302

@pytest.mark.django_db
def test_orderlists_view(client, user):
    response = client.get(reverse('orders'))
    assert response.status_code == 302

@pytest.mark.django_db
def test_product_view(client, products, user):
    client.login(username='michal', password='dupadupa')
    response = client.get(reverse('products'))
    assert response.status_code == 200
    ret_types = response.context['objects']
    assert list(ret_types) == products


@pytest.mark.django_db
def test_location_view(client, locations, user):
    client.login(username='michal', password='dupadupa')
    response = client.get(reverse('locations'))
    assert response.status_code == 200
    ret_types = response.context['objects']
    assert list(ret_types) == locations

@pytest.mark.django_db
def test_zone_view(client, zones, user):
    client.login(username='michal', password='dupadupa')
    response = client.get(reverse('zones'))
    assert response.status_code == 200
    ret_types = response.context['objects']
    assert list(ret_types) == zones

@pytest.mark.django_db
def test_stock_view(client, stock, user):
    client.login(username='michal', password='dupadupa')
    response = client.get(reverse('stocks'))
    assert response.status_code == 200
    ret_types = response.context['objects']
    assert list(ret_types) == stock


# @pytest.mark.django_db
# def test_orderlist_view(client, orderlists, user):
#     client.login(username='michal', password='dupadupa')
#     response = client.get(reverse('orders'))
#     assert response.status_code == 200
#     ret_types = response.context['objects']
#     assert ret_types[0] == orderlists[0]  #list(ret_types)==orderlist Expected :<OrderList: pjpopj, Kod systemowy produktu: 772186, BBD: 2020-10-10 w ilości 1>
                                                                    # Actual   :<OrderList: pjpopj, Kod systemowy produktu: 772186, BBD: 2020-10-10 w ilości 1>