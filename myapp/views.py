from django.http import JsonResponse
from .models import Product, CartItem, Profile, Order, OrderItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product, CartItem, Profile
from .forms import RegisterForm, ProfileUpdateForm

def index_view(request):
    supplements = Product.objects.filter(category='SUPP')
    memberships = Product.objects.filter(category='MEMB')
    return render(request, 'gym/index.html', {'supplements': supplements, 'memberships': memberships})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            

            Profile.objects.create(
                user=user,
                phone=form.cleaned_data['phone']
            )
            
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'gym/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'gym/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():

            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            

            profile.phone = form.cleaned_data['phone']
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            profile.save()
            
            messages.success(request, "Профилот е успешно ажуриран!")
            return redirect('profile')
    else:

        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = ProfileUpdateForm(instance=profile, initial=initial_data)

    return render(request, 'gym/profile.html', {'user': request.user, 'profile': profile, 'form': form})


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'gym/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == 'true' or True:
        return JsonResponse({
            'success': True,
            'message': f"Успешно додадовте {product.name} во кошничката!"
        })
        

    return redirect('supplements_page')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout_view(request):

    membership_id = request.GET.get('membership_id')
    direct_membership = None
    
    if membership_id:
        direct_membership = get_object_or_404(Product, id=membership_id, category='MEMB')
        cart_items = []
        total = direct_membership.price
    else:
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            messages.error(request, "Вашата кошничка е празна. Додадете продукти пред да одите на плаќање.")
            return redirect('cart')
        total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        

        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            phone=phone,
            total_amount=total
        )
        

        if direct_membership:
            OrderItem.objects.create(
                order=order,
                product=direct_membership,
                quantity=1,
                price=direct_membership.price
            )

            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.membership_status = 'Active'
            profile.membership_plan = direct_membership.name
            profile.save()
            
            messages.success(request, f"Успешно го активиравте членството: {direct_membership.name}!")
        else:

            has_membership = False
            membership_name = ""
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                if item.product.category == 'MEMB':
                    has_membership = True
                    membership_name = item.product.name

            if has_membership:
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.membership_status = 'Active'
                profile.membership_plan = membership_name
                profile.save()

            cart_items.delete()
        
        return render(request, 'gym/checkout_success.html')
        
    profile = getattr(request.user, 'profile', None)
    context = {
        'cart_items': cart_items,
        'direct_membership': direct_membership,
        'total': total,
        'profile': profile
    }
    return render(request, 'gym/checkout.html', context)

def supplements_page_view(request):
    supplements = Product.objects.filter(category='SUPP')
    return render(request, 'gym/supplements.html', {'supplements': supplements})

@user_passes_test(lambda u: u.is_superuser)
def add_product_action(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        Product.objects.create(name=name, description=description, price=price, category='SUPP', image=image)
        messages.success(request, "Суплементот е успешно додаден!")
    return redirect('supplements_page')

@user_passes_test(lambda u: u.is_superuser)
def delete_product_action(request, product_id):
    product = get_object_or_404(Product, id=product_id, category='SUPP')
    product.delete()
    messages.success(request, "Суплементот е успешно избришан!")
    return redirect('supplements_page')

@user_passes_test(lambda u: u.is_superuser)
def add_membership_action(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        Product.objects.create(name=name, description=description, price=price, category='MEMB')
        messages.success(request, "Членството е успешно додадено!")
    return redirect('index')

@user_passes_test(lambda u: u.is_superuser)
def delete_membership_action(request, product_id):
    product = get_object_or_404(Product, id=product_id, category='MEMB')
    product.delete()
    messages.success(request, "Членството е успешно избришано!")
    return redirect('index')

@login_required
def decrease_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f"Decreased quantity of {cart_item.product.name}.")
    else:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"Added {product.name} to your cart!")
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

@user_passes_test(lambda u: u.is_superuser)
def edit_product_action(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, category='SUPP')
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')

        if 'image' in request.FILES:
            product.image = request.FILES['image']
            
        product.save()
        messages.success(request, f"Суплементот '{product.name}' е успешно ажуриран!")
        
    return redirect('supplements_page')

@login_required
def cancel_membership_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if profile.membership_status == 'Active':
        old_plan = profile.membership_plan
        profile.membership_status = 'Inactive'
        profile.membership_plan = "No Membership"
        profile.save()
        messages.success(request, f"Успешно го откажавте членството ({old_plan}).")
    else:
        messages.error(request, "Немате активно членство за откажување.")
        
    return redirect('profile')

def about_view(request):
    return render(request, 'gym/about.html')