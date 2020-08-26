from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from wms.forms import LocationForm, ZoneForm, ProductForm, StockForm, OrderListForm, CartForm
from wms.models import Location, Zone, Product, Stock, OrderList, Cart


def index(request):
    return render(request, 'index.html')


class ProductView(PermissionRequiredMixin, View):
    permission_required = ['wms.view_product']

    def get(self, request, pk=None):
        products = Product.objects.all()
        if pk is None:
            form = ProductForm()
        else:
            b = Product.objects.get(pk=pk)
            form = ProductForm(instance=b)
        return render(request, 'detail_product_view.html', {'form': form, 'objects': products})

    def post(self, request, pk=None):
        if pk is None:
            form = ProductForm(request.POST)
        else:
            b = Product.objects.get(pk=pk)
            form = ProductForm(request.POST, instance=b)
        if form.is_valid():
            obj = form.save()
            if pk is None:
                return redirect(reverse("products"))
            else:
                return redirect(reverse_lazy("products", args=(pk,)))
        return render(request, 'detail_product_view.html', {'form': form})


class ProductDeleteView(PermissionRequiredMixin, View):
    permission_required = ['wms.delete_product']

    def get(self, request, pk):
        return render(request, 'delete_view.html', {'obj': Product.objects.get(pk=pk)})

    def post(self, request, pk):
        if request.POST['delete'] == 'Tak':
            Product.objects.get(pk=pk).delete()
        return redirect(reverse('products'))


class LocationView(PermissionRequiredMixin, View):
    permission_required = ['wms.view_location']

    def get(self, request, pk=None):
        locations = Location.objects.all()
        if pk is None:
            form = LocationForm()
        else:
            b = Location.objects.get(pk=pk)
            form = LocationForm(instance=b)
        return render(request, 'detail_view.html', {'form': form, 'objects': locations})

    def post(self, request, pk=None):
        if pk is None:
            form = LocationForm(request.POST)
        else:
            b = Location.objects.get(pk=pk)
            form = LocationForm(request.POST, instance=b)

        if form.is_valid():
            obj = form.save()
            if pk is None:
                return redirect(reverse("locations"))
            else:
                return redirect(reverse_lazy("locations", args=(pk,)))
        return render(request, 'detail_view.html', {'form': form})


class LocationDeleteView(PermissionRequiredMixin, View):
    permission_required = ['wms.delete_location']

    def get(self, request, pk):
        return render(request, 'delete_view.html', {'obj': Location.objects.get(pk=pk)})

    def post(self, request, pk):
        if request.POST['delete'] == 'Tak':
            Location.objects.get(pk=pk).delete()
        return redirect(reverse('locations'))


class ZoneView(PermissionRequiredMixin, View):
    permission_required = ['wms.view_zone']

    def get(self, request, pk=None):
        zones = Zone.objects.all()
        if pk is None:
            form = ZoneForm()
        else:
            b = Zone.objects.get(pk=pk)
            form = ZoneForm(instance=b)
        return render(request, 'detail_view.html', {'form': form, 'objects': zones})

    def post(self, request, pk=None):
        if pk is None:
            form = ZoneForm(request.POST)
        else:
            b = Zone.objects.get(pk=pk)
            form = ZoneForm(request.POST, instance=b)

        if form.is_valid():
            obj = form.save()
            if pk is None:
                return redirect(reverse("zones"))
            else:
                return redirect(reverse_lazy("zones", args=(pk,)))
        return render(request, 'detail_view.html', {'form': form})


class ZoneDeleteView(PermissionRequiredMixin, View):
    permission_required = ['wms.delete_zone']

    def get(self, request, pk):
        return render(request, 'delete_view.html', {'obj': Zone.objects.get(pk=pk)})

    def post(self, request, pk):
        if request.POST['delete'] == 'Tak':
            Zone.objects.get(pk=pk).delete()
        return redirect(reverse('zones'))


class StockView(PermissionRequiredMixin, View):
    permission_required = ['wms.view_stock']

    def get(self, request, pk=None):
        stocks = Stock.objects.all()
        if pk is None:
            form = StockForm()
        else:
            b = Stock.objects.get(pk=pk)
            form = StockForm(instance=b)
        return render(request, 'detail_view.html', {'form': form, 'objects': stocks})

    def post(self, request, pk=None):
        if pk is None:
            form = StockForm(request.POST)
        else:
            b = Stock.objects.get(pk=pk)
            form = StockForm(request.POST, instance=b)

        if form.is_valid():
            obj = form.save()
            if pk is None:
                return redirect(reverse("stocks"))
            else:
                return redirect(reverse_lazy("stocks", args=(pk,)))
        return render(request, 'detail_view.html', {'form': form})


class StockDeleteView(PermissionRequiredMixin, View):
    permission_required = ['wms.delete_stock']

    def get(self, request, pk):
        return render(request, 'delete_view.html', {'obj': Stock.objects.get(pk=pk)})

    def post(self, request, pk):
        if request.POST['delete'] == 'Tak':
            Stock.objects.get(pk=pk).delete()
        return redirect(reverse('stocks'))


class DetailCartView(PermissionRequiredMixin, View):
    permission_required = ['wms.view_cart']

    def get(self, request):
        form = CartForm()
        cart,temp = Cart.objects.get_or_create(user=request.user)
        return render(request, 'detail_view_cart.html', {'form':form, 'cart': cart})

    def post(self, request, pk=None):
        if pk is None:
            form = CartForm(request.POST)
        else:
            a = Cart.objects.get(pk=pk)
            form = CartForm(request.POST, instance=a)
        if form.is_valid():
            obj = form.save()
            if pk is None:
                return redirect(reverse("carts"))
            else:
                return redirect(reverse_lazy("carts", args=(pk,)))
        return render(request, 'detail_view.html', {'form': form})


class OrderListView(PermissionRequiredMixin, View):
    permission_required = ['wms.view_orderlist']

    def get(self, request, pk=None):
        cart, created= Cart.objects.get_or_create(user=request.user)
        if pk is None:
            form = OrderListForm()
        else:
            b = OrderList.objects.get(pk=pk)
            form = OrderListForm(instance=b)
        return render(request, 'detail_view.html', {'form': form, 'objects': cart.orderlist_set.all()})

    def post(self, request, pk=None):
        if pk is None:
            form = OrderListForm(request.POST)
        else:
            b = OrderList.objects.get(pk=pk)
            form = OrderListForm(request.POST, instance=b)

        if form.is_valid():
            b = form.save(commit=False)
            user = request.user
            b.cart = user.cart
            b.save()
            if pk is None:
                return redirect(reverse("orders"))
            else:
                return redirect(reverse_lazy("orders", args=(pk,)))
        return render(request, 'detail_view.html', {'form': form})


class OrderListDeleteView(PermissionRequiredMixin, View):
    permission_required = ['wms.delete_orderlist']

    def get(self, request, pk):
        return render(request, 'delete_view.html', {'obj': OrderList.objects.get(pk=pk)})

    def post(self, request, pk):
        if request.POST['delete'] == 'Tak':
            OrderList.objects.get(pk=pk).delete()
        return redirect(reverse('orders'))
