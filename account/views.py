from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .models import *
from .forms import *
from .filters import *
from .decorators import *

# Create your views here.


def home(request):
    return render(request, 'base.html')


@unauthenticated_user
def registrationPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            # Customer.objects.create(
            #     user=user,
            #     name = user.username,
            # )

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'account/register.html', context)


@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'username or password is incorrect')

    context = {}
    return render(request, 'account/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
                'orders': orders,
                'customers': customers,
                'total_orders': total_orders,
                'delivered': delivered,
                'pending': pending,
                }
                
    return render(request, 'account/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
                'orders': orders,
                'total_orders': total_orders,
                'delivered': delivered,
                'pending': pending,
                }
    return render(request, 'account/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('user_settings')

    context = {'form': form}
    return render(request, 'account/user_settings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {'products': products, }
    return render(request, 'account/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, idnum):
    customer = Customer.objects.get(id=idnum)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
                'customer': customer,
                'orders': orders,
                'order_count': order_count,
                'myFilter': myFilter,
                }
    return render(request, 'account/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, idnum):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=idnum)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')

    context = {'formset': formset, 'customer': customer}
    return render(request, 'account/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, idnum):

    order = Order.objects.get(id=idnum)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'account/update_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, idnum):
    order = Order.objects.get(id=idnum)
    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')

    context = {'item': order}
    return render(request, 'account/delete.html', context)
