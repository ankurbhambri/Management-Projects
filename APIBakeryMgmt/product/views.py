from functools import reduce
from datetime import datetime
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from product.models import Product
from accounts.models import OrderHistory


def try_or(fn, default, *args, **kwargs):
    """
    Usage: try_or(lambda: request_user.email, None, *args, **kwargs)
    """
    try:
        return fn(*args, **kwargs)
    except Exception:
        return default


class ProductViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = (AllowAny, )

    def list(self, request):
        product = list()
        all_products = Product.objects.all()
        if all_products:
            for i in all_products:
                ingredient_obj = i.ingredient_set.all()
                product_obj = {
                    'id': i.id,
                    'product_name': i.product_name,
                    'author': i.author,
                    'price': i.marked_price,
                    'discount %': i.discount,
                    'final_price': i.selling_price,
                    'product_ingredients': []
                }
                if ingredient_obj:
                    for obj in ingredient_obj:
                        product_obj['product_ingredients'].append({
                            'material_name':obj.material_name.item_name,
                            'material_quantity_used':obj.qty,
                        })
                product.append(product_obj)
            return Response(product)
        return Response("No Data Exists.")

    def retrieve(self, request, pk):
        product = list()
        if pk:
            prod_obj = Product.objects.filter(pk=pk)
            if prod_obj:
                ingredient_obj = prod_obj[0].ingredient_set.all()
                product_obj = {
                    'id': prod_obj[0].id,
                    'product_name': prod_obj[0].product_name,
                    'author': prod_obj[0].author,
                    'price': i.marked_price,
                    'discount %': i.discount,
                    'final_price': i.selling_price,
                    'product_ingredients': []
                }
                if ingredient_obj:
                    for obj in ingredient_obj:
                        product_obj['product_ingredients'].append({
                            'material_name':obj.material_name.item_name,
                            'material_quantity_used':obj.qty,
                        })
                product.append(product_obj)
                return Response(product)
            else:
                return Response("No data exists with this id !")


class PlaceOrder(viewsets.ViewSet):
    """A viewset for placing order for a user."""

    permission_classes = (IsAuthenticated, )

    def create(self, request):
        product_details = Product.objects.filter(
            reduce(lambda x, y: x | y, [Q(
                product_name__contains=word) for word in self.request.data['product_name']]))
        order_list = []
        if product_details:
            for i in product_details:
                order_details = {
                    'product_name': i.product_name,
                    'marked price': i.marked_price,
                    'discount %': i.discount,
                    'final_price': i.selling_price,
                }
                order_list.append(order_details)
            OrderHistory.objects.create(user=self.request.user, order=order_list)
            return Response(order_list)
        else:
            return Response('No Product is avaliable with this name kindly check !')


class OrdersHistory(viewsets.ViewSet):
    """A viewset for viewing order history of a user."""

    permission_classes = (IsAuthenticated, )

    def list(self, request):
        history = OrderHistory.objects.filter(
                user=self.request.user)
        order_history = []
        if history:
            for i in history:
                order_history.append(i.order)
            return Response(order_history)
        else:
            return Response('No Product is avaliable with this name kindly check !')


class SalesReport(viewsets.ViewSet):
    """
    A viewset for viewing sales report.
    {
        "datetime format" : YYYY-MM-DD
    }
    """
    permission_classes = (IsAuthenticated, )

    def create(self, request):
        start_date = try_or(lambda: datetime.strptime(
            self.request.data['start_date'], '%Y-%m-%d'), datetime.now())
        end_date = try_or(lambda: datetime.strptime(
            self.request.data['end_date'], '%Y-%m-%d'), datetime.now())
        total_earnings = 0
        sold_product = []
        if self.request.user.is_superuser:
            history = OrderHistory.objects.filter(
                created_at__range=[start_date, end_date])
            product_history = {}
            if history:
                for order in history:
                    for obj in order.order:
                        total_earnings += obj['final_price']
                        if obj['product_name'] not in product_history.items():
                            product_history[obj['product_name']] = obj['final_price']
                        else:
                            product_history[obj['product_name']] += obj['final_price']
                    
                        sold_product.append(obj['product_name'])
                sales_report = {
                    'total_earnings': total_earnings,
                    'most_selling_product': max(product_history, key=product_history.get),
                    'total_earning_most_selling_product': max(product_history.values()),
                    'least_selling_product': min(product_history, key=product_history.get),
                    'total_earning_least_selling_product': min(product_history.values()),
                }
                return Response(sales_report)
            else:
                return Response('No Sales avaliable in provided date')
        else:
            return Response('Only Permission to Superuser')
