from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Cart.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.get_total_price() for item in items)
    return render(request, 'store/cart.html', {'cart': cart, 'items': items, 'total': total})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    cart_item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    if not items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('home')

    total = sum(item.get_total_price() for item in items)
    
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=total, status='Pending')
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
        # Clear cart
        items.delete()
        messages.success(request, f"Order #{order.order_number} placed successfully!")
        return redirect('home')
        
    return render(request, 'store/checkout.html', {'items': items, 'total': total})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})
