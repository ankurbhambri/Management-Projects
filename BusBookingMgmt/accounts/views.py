from django.views.generic import FormView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import SignUpForm


class RegisterView(FormView):

    template_name = 'registration/register.html'
    form_class = UserCreationForm

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = {}
        context['redirect_url'] = self.request.GET.get('next')
        form = SignUpForm()
        context['form'] = form
        context['error'] = request.session.get('signup')
        return render(request, self.template_name, {'context': context})

    def post(self, request, *args, **kwargs):
        context = {}
        form = SignUpForm(request.POST)
        context['form'] = form
        redirect_url = request.POST.get('nexturl')
        if form.is_valid():
            form.save()
        else:
            request.session['signup'] = form.errors
            return redirect(self.request.get_full_path() + '?next=' + redirect_url)
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
        if user:
            login(request, user)
            return redirect(redirect_url)
        return render(request, self.template_name, {'context': context})


class LoginView(ListView):

    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = {}
        context['redirect_url'] = self.request.GET.get('next')
        context['error'] = request.session.get('resp')
        return render(request, self.template_name, {'context': context})

    def post(self, request, *args, **kwargs):
        redirect_url = request.POST.get('nexturl')
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect(redirect_url)
        else:
            request.session['resp'] = 'username and password does not matched!'
            return redirect(self.request.get_full_path() + '?next=' + redirect_url)
        return render(request, self.template_name, {})


def logout_request(request):
    logout(request)
    return redirect("/")
