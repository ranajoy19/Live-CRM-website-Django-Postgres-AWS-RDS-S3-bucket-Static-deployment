from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from .models import *
from .form import OrderForm,CreateUserForm,CustomerForm
from .filtters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorator import unauthenticated_user,admin_only,allowed_user
from django.contrib.auth.models import Group

# Create your views here.

@unauthenticated_user

def register(request):
    userform=CreateUserForm()
    if request.method=="POST":
            userform=CreateUserForm(request.POST)
            if userform.is_valid():
                user=userform.save()

                # add new registration to the Customer Group

                group =Group.objects.get(name='customer')

                user.groups.add(group)

                #add user to the customer automatically
                Customer.objects.create(user=user,name=user.username)



                # to get only the user name from userform
                username =userform.cleaned_data.get('username')
                # flash massage after successfully register
                messages.success(request,'Accounts was created '+ username)
                return redirect('login')


    content={'userform':userform}
    return render(request, 'register.html',content)


@unauthenticated_user

def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')

    return render(request,'login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def Home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    orders_total= orders.count()
    orders_delivered= orders.filter(status='Delivery').count()
    orders_pending=orders.filter(status='Pending').count()

    content ={'order':orders,'customer':customers,'orders_total':orders_total,
              'orders_delivered':orders_delivered,'orders_pending':orders_pending}

    return render(request,'dashboard.html',content)

@admin_only
@login_required(login_url='login')
def Products(request):
    products = Product.objects.all()


    return render(request,'Products.html',{'product':products})

@allowed_user(allowed_roles=['admin'])
@login_required(login_url='login')
def Customers(request,pk):
    customers=Customer.objects.get(id=pk)


    orders=customers.order_set.all()
    orders_total= orders.count()

    myfilter =OrderFilter(request.GET,queryset=orders)

    orders=myfilter.qs


    content={'customers':customers,'order':orders,'orders_total':orders_total,'myfilter':myfilter}
    return render(request,'Customer.html',content)


@allowed_user(allowed_roles=['admin'])
@login_required(login_url='login')
def CreateOrder(request,pk):
    OrderFormSet =inlineformset_factory(Customer,Order,fields=('products','status'))
    customer =Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset= Order.objects.none() ,instance=customer)
    if request.method =='POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    content={'formset':formset}
    return render(request,'form.html',content)

@allowed_user(allowed_roles=['admin'])
@login_required(login_url='login')
def update(request,pk):

    order=Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method =='POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    content={'formset':form}
    return render(request,'form.html',content)



def delete(request,pk):
    order=Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    content={'item':order}

    return render(request,'delete.html',content)




@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])

def UserPage(request):
    orders=request.user.customer.order_set.all()
    orders_total = orders.count()
    orders_delivered = orders.filter(status='Delivery').count()
    orders_pending = orders.filter(status='Pending').count()

    content ={'order':orders,'orders_total':orders_total,
              'orders_delivered':orders_delivered,'orders_pending':orders_pending}

    return render(request,'user.html',content)



@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])

def Setting(request):
    customer=request.user.customer

    form =CustomerForm(instance=customer)

    if request.method =="POST":
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    content={'form':form}

    return render(request,'setting.html',content)

