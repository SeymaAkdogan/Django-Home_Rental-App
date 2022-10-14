
from django.shortcuts import redirect, render
from cart.models import CartItem, Cart
from datetime import datetime
from home.models import Home


def checkDates(user_start_time, user_end_time, home_start_time, home_end_time):
    date_format = "%Y-%m-%d"
    user_end_time_ = datetime.strptime(str(user_end_time), date_format)
    user_start_time_ = datetime.strptime(str(user_start_time), date_format)
    home_start_time_ = datetime.strptime(str(home_start_time), date_format)
    home_end_time_ = datetime.strptime(str(home_end_time), date_format)

    if user_start_time_ > user_end_time_ or user_end_time_ == user_start_time_ or home_start_time_ > user_end_time_ or home_end_time_ < user_start_time_ or user_end_time_ > home_end_time_ or datetime.now() > user_end_time_ or datetime.now() > user_start_time_:
        return False
    else:
        return True


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_price = 0
        if cart:
            cartItems = CartItem.objects.filter(cart=cart[0])
            for cartItem in cartItems:
                total_price += float(cartItem.price)
            return render(request, 'cart/cartList.html', {
                'cartItems': cartItems,
                'total_price': total_price
            })
        else:
            return render(request, 'cart/cartList.html')
    else:
        return redirect('login')


def add_to_cart(request, id):
    if request.user.is_authenticated:
        home = Home.objects.get(id=id)
        cart = Cart.objects.filter(user=request.user)

        if checkDates(request.GET.get('start_time', None),request.GET.get('end_time', None),home.start_time,home.end_time) == False:
            return render(request, 'home/detail.html', {
                'home': home,
                'error': "Please Check Date Fields"
            })
        
        if home.owner.id == request.user.id:
            return render(request, 'home/detail.html', {
                'home': home,
                'error': "You Cannot Reserve Your House"
            })

        delta = datetime.strptime(str(request.GET.get('end_time', None)), "%Y-%m-%d") - datetime.strptime(str(request.GET.get('start_time', None)), "%Y-%m-%d")
        if cart:
            home_count = CartItem.objects.filter(home=home, cart=cart[0])
            if home_count:
                return render(request,'home/detail.html',{
                    'home' : home,
                    'error' : "You Already Have a Reservation For This House"
                })
            else:
                cartItem = CartItem.objects.create(home=home, start_time=request.GET.get(
                    'start_time', None), end_time=request.GET.get('end_time', None), price=home.price * delta.days, cart=cart[0])
                cartItem.save()
        else:
            cart = Cart.objects.create(user=request.user)
            cart.save()
            cartItem = CartItem.objects.create(home=home, start_time=request.GET.get(
                'start_time', None), end_time=request.GET.get('end_time', None), price=home.price * delta.days, cart=cart)
            cartItem.save()

        return redirect('reservations')
    else:
        return redirect('login')


def editCart(request, id):
    home = Home.objects.get(id=id)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cartItem = CartItem.objects.get(cart=cart[0], home=home)

        if checkDates(request.GET.get('start_time', None),request.GET.get('end_time', None),home.start_time,home.end_time) == False:
            cart = Cart.objects.filter(user=request.user)
            total_price = 0
            if cart:
                cartItems = CartItem.objects.filter(cart=cart[0])
                for cartItem in cartItems:
                    total_price += float(cartItem.price)
                return render(request, 'cart/cartList.html', {
                    'cartItems': cartItems,
                    'total_price': total_price,
                    'error': "Please Check Date Fields"
                })
            else:
                return render(request, 'cart/cartList.html')
            

        cartItem.start_time = request.GET.get('start_time', None)
        cartItem.end_time = request.GET.get('end_time', None)
        cartItem.save()
        return redirect('reservations')
    else:
        return redirect('login')


def remove_from_cart(request, id):
    if request.user.is_authenticated:
        home = Home.objects.get(id=id)
        cart = Cart.objects.filter(user=request.user)
        if cart:
            deleted_item = CartItem.objects.get(home=home, cart=cart[0])
            if deleted_item is not None:
                deleted_item.delete()

        return redirect('reservations')
    else:
        return redirect('login')
