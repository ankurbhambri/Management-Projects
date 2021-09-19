from django.shortcuts import render
from django.views.generic import ListView
from orders.models import OrderTable


class OrderPageView(ListView):
    model = OrderTable
    template_name = 'orders/orderview.html'

    def get_context_data(self, **kwargs):
        context = super(OrderPageView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = dict()
        context['login_user'] = self.request.user.username
        user_orders = OrderTable.objects.filter(user=self.request.user)
        context['user_orders'] = user_orders
        return render(request, self.template_name, {'context': context})

    def post(self, request, *args, **kwargs):
        context = dict()
        if request.POST.get('onward_side'):
            order_id = OrderTable.objects.filter(
                id=int(request.POST.get('onward_side')))[0]
            order_id.query.attrs.pop('one_side')
            order_id.query.save()
        elif request.POST.get('return_side'):
            order_id = OrderTable.objects.filter(
                id=int(request.POST.get('return_side')))[0]
            order_id.query.attrs.pop('return_query')
            order_id.query.save()
        user_orders = OrderTable.objects.filter(user=self.request.user)
        context['user_orders'] = user_orders
        context['login_user'] = self.request.user.username
        return render(request, self.template_name, {'context': context})
