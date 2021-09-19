import re
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView
from booking.models import BusService, BusTiming, Query
from orders.models import OrderTable


class HomePageView(TemplateView):

    template_name = "booking/index.html"
    model = BusService

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        values = BusService.objects.values_list('source', 'destination')
        chain_dict = {}
        for key, value in values:
            if key not in chain_dict.keys():
                chain_dict[key] = [value]
            else:
                chain_dict[key].append(value)
        context['chain_dict'] = chain_dict
        context['login_user'] = self.request.user.username
        return context


class BookingListView(ListView):

    model = BusTiming
    template_name = "booking/bookinglist.html"

    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        response_data = dict()
        query_dict = dict()
        choice1 = request.POST.get('choice1')
        choice2 = request.POST.get('choice2')
        passenger = request.POST.get('passenger')
        date = request.POST.get('date')

        one_side_query = BusTiming.objects.filter(
            service__source=choice1, service__destination=choice2,
            service__passanger_capacity__gte=passenger)

        if one_side_query:
            query_dict['one_side'] = {
                'source': choice1,
                'destination': choice2,
                'passenger': int(passenger),
                'journey_date': date,
                'vehicle_name': one_side_query[0].service.vehicle.vehicle_name,
                'departure_location': one_side_query[0].service.souce_bus_stand_location,
                'arival_location': one_side_query[0].service.destination_bus_stand_location,
                'departure_time': one_side_query[0].departure_time.strftime("%H:%M:%S:%P"),
                'desstination_time': one_side_query[0].desstination_time.strftime("%H:%M:%S:%P"),
                'total_price': int(passenger) * int(one_side_query[0].service.per_passanger_price),
                'ac': 'Air Conditioned' if one_side_query[0].service.vehicle.ac else 'Non AC'}

        return_query = BusTiming.objects.filter(
            service__source=choice2, service__destination=choice1,
            service__passanger_capacity__gte=passenger)

        if return_query:
            query_dict['return_query'] = {
                'source': choice2,
                'destination': choice1,
                'passenger': int(passenger),
                'journey_date': date,
                'vehicle_name': return_query[0].service.vehicle.vehicle_name,
                'departure_location': return_query[0].service.souce_bus_stand_location,
                'arival_location': return_query[0].service.destination_bus_stand_location,
                'departure_time': return_query[0].departure_time.strftime("%H:%M:%S:%P"),
                'desstination_time': return_query[0].desstination_time.strftime("%H:%M:%S:%P"),
                'total_price': int(passenger) * int(return_query[0].service.per_passanger_price),
                'ac': 'Air Conditioned' if return_query[0].service.vehicle.ac else 'Non AC'}

        query_dict['amt'] = int(passenger) * int(one_side_query[0].service.per_passanger_price) + \
            int(passenger) * int(return_query[0].service.per_passanger_price)
        query_id = Query.objects.create(attrs=query_dict)
        response_data['one_side_query'] = one_side_query
        response_data['return_query'] = return_query
        response_data['query_id'] = query_id.id
        response_data['login_user'] = self.request.user.username
        return render(request, self.template_name, {"response_data": response_data})


class CheckoutView(DetailView):
    model = Query
    template_name = 'booking/checkout_page.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CheckoutView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = dict()
        path = self.request.get_full_path()
        query_id = re.findall('\d+', path)
        query_response = Query.objects.filter(id=int(query_id[0]))
        context = query_response[0].attrs
        context['login_user'] = self.request.user.username
        return render(request, self.template_name, {'context': context})

    def post(self, request, *args, **kwargs):
        context = dict()
        amt = 0
        query_response = Query.objects.filter(id=int(request.POST['query_id']))
        if request.POST.get('one_side'):
            context['one_side'] = query_response[0].attrs['one_side']
            amt += query_response[0].attrs['one_side']['total_price']
        if request.POST.get('return_side'):
            context['return_query'] = query_response[0].attrs['return_query']
            amt += query_response[0].attrs['one_side']['total_price']
        context['amt'] = amt
        context['query_id'] = query_response[0].id
        context['login_user'] = self.request.user.username
        return render(request, self.template_name, {'context': context})


class SucessView(ListView):
    model = OrderTable
    template_name = 'booking/success_page.html'

    def get_context_data(self, **kwargs):
        context = super(SucessView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        query_id = int(request.POST['query_id'])
        query_obj = Query.objects.filter(id=query_id)
        order = OrderTable.objects.create(user=self.request.user,
                                          query=query_obj[0])
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        name = request.user.first_name + ' ' + request.user.last_name
        send_mail(
            'BusBooking',
            ' Hi, ' + name
            + '\n Confirmation on your order booking and thank you for choosing us your order id is ' +
            'bus' + str(order.id)
            + '\n Stay Safe and obey all corona virus methods',
            from_email,
            recipient_list, fail_silently=False)
        return render(request, self.template_name, {"order": order})
