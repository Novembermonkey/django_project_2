from webbrowser import Error

from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm, CustomerForm
from .models import Product, Category, Customer
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models.functions import Round
# Create your views here.

def index(request, category_title = None):
    categories = Category.objects.all()
    search_query = request.GET.get('q', '')

    products = Product.objects.all()


    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {'products': products,
               'categories': categories,
               }
    return render(request, 'shop/index.html', context=context)

def product_detail(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        comments = product.comments.all().order_by('-created_at')[:5]

        context = {'product': product, 'comments': comments}
        return render(request, 'shop/product-details.html', context=context)

    except Product.DoesNotExist:
        return HttpResponse(status=404, content='Product not found')


def product_list(request, category_name = None):
    products = Product.objects.all()
    search_query = request.GET.get('q', '')
    if category_name:
        category_id = Category.objects.get(name=category_name).id
        products = products.filter(category_id=category_id)

    if search_query:
        products = products.filter(name__icontains=search_query)

    products = products.annotate(avg_rating=Round(Avg('comments__rating'), precision=2))
    context = {'products': products,}

    return render(request, 'shop/product-list.html', context=context)

def add_comment(request, pk):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = get_object_or_404(Product, pk=pk)
            comment.save()
            messages.success(request, 'Comment added')
        return redirect('shop:product_detail', pk=pk)

    return render(request, 'shop/product-details.html', context={'form': form})





def customers_list(request):
    customers = Customer.objects.all()
    return render(request, 'shop/customers.html', context={'customers': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'shop/customer-details.html', context={'customer': customer})

@login_required
def customer_create(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop:customers')

    return render(request, 'shop/customer/create.html', context={'form': form})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('shop:customers')  # Update this to match your URL name
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'shop/customer/edit.html', {
        'form': form,
        'customer': customer,
    })

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('shop:customers')
    return render(request, 'shop/customer/delete.html', context={'customer': customer})

