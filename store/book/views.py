import json

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView

from .forms import ReviewForm
from .models import Book, Cart, Review


# from .models import CartItem
# Create your views here.

def homepage(request):
    return render(request,'homepage.html')

#### 1
class list1(ListView):
    model = Book
    fields =['title','author','description','price','image_url','review','book_available']
    context_object_name = 'lists'
    template_name = 'list1.html'









##################### authentication
###############
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not same!!")
        else:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

            return redirect("signin")
    return render(request, 'signup.html')



def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return HttpResponse("username or password is incorrect!!!")
    return render(request, 'login.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logout successfully.')
    return redirect('homepage')


class detail1(DetailView):
    model = Book
    fields=['title','author','description','price','image_url','book_available']
    template_name = 'detail1.html'
    context_object_name = 'every'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        return context








##############
############   payment
class BookCheckoutView(DetailView):
    model = Book
    fields = ['title','author','description','price','image_url','review','book_available']
    template_name = 'checkout.html'


def Paymentcomplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    product = Book.objects.get(id=body['prosuctId'])
    Order.objects.create(product=product)
    return JsonResponse('Payment completed', safe=False)


################
################## search
class SearchResultView(ListView):
    model = Book
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(Q(title=query)| Q(book_type=query))

####################
###################### filter
class Filter(ListView):
    model = Book
    template_name = 'filter.html'

    def get_queryset(self):
        query = self.request.GET.get('f')
        return Book.objects.filter(Q(book_type=query))



###############
################# cart


def add_to_cart(request, product_id):
    Product = get_object_or_404(Book, pk=product_id)
    cart_item,created = Cart.objects.get_or_create(
        user=request.user,
        product= Product,
        price=Product.price,
        image_url = Product.image_url,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


############### review
def add_review(request, pk):
    product = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('detail1', pk=product.pk)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'product': product})


def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
    return redirect('detail1', pk=review.product.pk)























