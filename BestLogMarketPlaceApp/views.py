from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm,ProfileForm
from .models import Category, Product,Transaction,BankPaymentDetail,Cart, CartItem
from django.db.models import Sum
from django.db.models import Count, Q
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.template.loader import render_to_string


# Create your views here.


def maintain(request):
    return render(request,'BestLogMarketPlaceApp/maintain.html')

from django.db.models import Count, Q

def home(request):
    # Get all categories with annotated product counts excluding approved transactions
    cart_item_count = get_cart_item_count(request)
    categories = Category.objects.prefetch_related(
        'products',
        'products__transactions'
    ).annotate(
        total_products=Count('products', filter=~Q(products__transactions__transaction_status='approved'))
    ).order_by('-order')  # Order by the 'order' field in descending order

    # Optionally filter categories based on a query parameter
    q = request.GET.get('q', '')
    if q and q != 'all':
        categories = categories.filter(
            Q(name__icontains=q) | Q(products__name__icontains=q)
        )

    no_categories_found = not categories.exists()

    # Adding the filtering logic for products directly
    for category in categories:
        category.filtered_products = category.products.exclude(transactions__transaction_status='approved')

    cart = get_or_create_cart(request)
    cart_product_ids = cart.items.values_list('product_id', flat=True)

    context = {
        'categories': categories,
        'q': q,
        'no_categories_found': no_categories_found,
        'cart_item_count': cart_item_count,
        'cart_product_ids': cart_product_ids,
    }
    return render(request, 'BestLogMarketPlaceApp/index.html', context)

def category_products_view(request, category_id):
    # Fetch the specific category or return 404 if not found
    category = get_object_or_404(Category, id=category_id)

    # Fetch products that are not linked to an "approved" transaction
    products = category.products.filter(
        ~Q(transactions__transaction_status='approved')
    ).distinct()
    cart = get_or_create_cart(request)
    # Get all product IDs in the cart
    cart_product_ids = cart.items.values_list('product_id', flat=True)

    # Pass the category and filtered products to the template
    context = {
        'category': category,
        'products': products,
        'cart_product_ids': cart_product_ids,
    }
    return render(request, 'BestLogMarketPlaceApp/category_products.html', context)

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Session-based cart for guest users
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
            if not cart:
                cart = Cart.objects.create()  # Create a new Cart object
                request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.create()  # Create new Cart object
            request.session['cart_id'] = cart.id
    return cart

def get_cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.filter(id=cart_id).first() if cart_id else None

        # Use session-based cart item count if it's stored
        if cart and 'cart_item_count' not in request.session:
            request.session['cart_item_count'] = cart.items.count()

    return request.session.get('cart_item_count', 0) if not request.user.is_authenticated else cart.items.count() if cart else 0




def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    # Get or create the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Update the session cart item count for non-authenticated users
    if not request.user.is_authenticated:
        request.session['cart_item_count'] = cart.items.count()  # Update session with the correct count

    # Display success message and redirect
    messages.success(request, f'Added {product.name} to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def view_cart(request):
    cart = get_or_create_cart(request)
    return render(request, 'BestLogMarketPlaceApp/cart.html', {'cart': cart})

def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')


def about(request):
    return render(request, 'BestLogMarketPlaceApp/p_about.html')


def contact(request):
    return render(request, 'BestLogMarketPlaceApp/contact.html')

@login_required(login_url='/home')
def dashboard(request):
    orders = Transaction.objects.filter(user=request.user, transaction_status='approved').prefetch_related('products')
    order_count = orders.count()
    total_amount_paid = orders.aggregate(Sum('amount'))['amount__sum'] or 0.0
    context = {
        'orders': orders,
        'order_count': order_count,
        'total_amount_paid': total_amount_paid,
    }
    return render(request, 'BestLogMarketPlaceApp/Dashboard.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()  # Save the user before authenticating
                login(request, user)
                messages.success(request, f'Account created for {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Error creating account. Please check the form.')
        else:
            form = RegisterForm()
    return render(request, 'BestLogMarketPlaceApp/register.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        error_message = None
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        return render(request, 'BestLogMarketPlaceApp/login.html', {'error_message': error_message})


def logout_user(request):
    logout(request)
    return redirect('home')

def profile_page(request):
    # if request.method == 'POST':
    #     form = ProfileForm(request.POST, request.FILES, instance=request.user)
    #     if form.is_valid():
    #         form.save()
#         return redirect('dashboard')
    # else:
    #     form = ProfileForm(instance=request.user)
    # return render(request, 'CoinacadeApp/dashboard/profile_page.html', {'form': form})
    return render(request, 'BestLogMarketPlaceApp/profile-setting.html')

def pending(request):
    payment_status = request.GET.get('status')
    tx_ref = request.GET.get('tx_ref')

    # Retrieve the customer email from the query parameter
    customer_email = request.GET.get('email')

    cart = get_or_create_cart(request)

    if payment_status == 'successful' or payment_status == 'completed':
        transaction_status = 'approved'
    else:
        transaction_status = 'declined'

    transaction = Transaction.objects.create(
        user=request.user if request.user.is_authenticated else None,  # Handle anonymous users
        amount=cart.total_price(),
        transaction_status=transaction_status,
        tx_ref=tx_ref
    )

    for item in cart.items.all():
        transaction.products.add(item.product)

    transaction.save()

    if transaction_status == 'approved':
        cart_items = cart.items.all()

        # Send email to the customer
        if customer_email:
            subject = "Your Purchase Details"
            product_details = "\n".join([f"{item.product.name}: {item.product.account_details}" for item in cart_items])
            message = f"Thank you for your purchase. Here are the product details:\n\n{product_details}\n\nBest regards,\nBestLog Marketplace Team"
            from_email = 'bestlogsmarketplace@gmail.com'
            recipient_list = [customer_email]

            send_mail(subject, message, from_email, recipient_list)

        cart.items.all().delete()

    return render(request, 'BestLogMarketPlaceApp/pending.html', {
        'transaction_status': transaction_status,
        'transaction': transaction,
        'payment_status': payment_status
    })

def payment_page(request):
    cart = get_or_create_cart(request)
    bank_payment_details = BankPaymentDetail.objects.get(active=True)

    if request.method == 'POST':
        # Save the customer email in session
        customer_email = request.POST.get('customer[email]')
        request.session['customer_email'] = customer_email  # Save email in session

        if request.user.is_authenticated:
            transaction = Transaction.objects.create(
                user=request.user,
                amount=cart.total_price(),
                transaction_status='pending',
            )
        else:
            transaction = Transaction.objects.create(
                user=None,  # No user for anonymous purchase
                amount=cart.total_price(),
                transaction_status='pending',
            )
        for item in cart.items.all():
            transaction.products.add(item.product)
        transaction.save()

        cart.items.all().delete()  # Clear the cart after purchase
        return redirect('pending')

    return render(request, 'BestLogMarketPlaceApp/payment_page.html', {'cart': cart, 'bank_payment_details': bank_payment_details})


@login_required(login_url='/login_user')
def payment_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    context = {'transactions': transactions}
    return render(request, 'BestLogMarketPlaceApp/payment_history.html', context)

@login_required(login_url='/login_user')
def orders(request):
    orders = Transaction.objects.filter(user=request.user, transaction_status='approved')
    context = {'orders': orders}
    return render(request, "BestLogMarketPlaceApp/orders.html", context)

@login_required(login_url='/login_user')
def order_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product }
    return render(request,"BestLogMarketPlaceApp/order_detail.html", context)

def profile_page(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'BestLogMarketPlaceApp/profile-setting.html', {'form': form})

def privacy_page(request):
    return render (request,'BestLogMarketPlaceApp/privacy.html' )

def terms_page(request):
    return render (request,'BestLogMarketPlaceApp/terms_page.html' )

def rules_page(request):
    return render (request,'BestLogMarketPlaceApp/rules.html' )

# def search_products(request):
#   search_query = request.GET.get('search', '')  # Get the search query from URL parameters

#   if search_query:
#     # Filter categories by name (case-insensitive)
#     categories = Category.objects.filter(name__icontains=search_query)
#     products = Product.objects.filter(category__in=categories)  # Find products in matching categories
#   else:
#     categories = Category.objects.all()
#     products = Product.objects.all()  # Display all categories and products if no query

#   context = {'categories': categories, 'products': products, 'search_query': search_query}
#   return render(request, 'BestLogMarketPlaceApp/index.html', context)