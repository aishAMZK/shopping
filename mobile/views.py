
from django.shortcuts import render, redirect

from django.contrib.auth.hashers import make_password, check_password


from .models import Product, Customer
from django.views import View
from .models import Order
# Create your views here.



class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])

        return redirect('homepage')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        products = None
        prds = Product.get_all_products()
        # return render(request, 'mobile/order.html')

        return render(request, 'mobile/index.html', {'products': prds})






class Signup(View):
    def get(self, request):
        return render(request, 'mobile/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)

        error_message = self.validateCustomer(customer)

        # saving
        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
            customer.register()
            return redirect('homepage')

        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'mobile/signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "First Name Required.."
        elif len(customer.first_name) < 4:
            error_message = "First Name must be 4 char long or more"
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 1:
            error_message = "Last Name must be 1 char long or more"
        elif not customer.phone:
            error_message = 'Phone Number Required'
        elif len(customer.phone) < 10:
            error_message = "Phone Number must be 10 char long"
        elif len(customer.password) < 6:
            error_message = "Password must be 6 char long"
        elif len(customer.email) < 5:
            error_message = "Email must be 5 char long"
        elif customer.isExists():
            error_message = 'Email Address Already Registered'

        return error_message


class Login(View):
    def get(self, request):
        return render(request, 'mobile/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            #     if flag:
            request.session['customer'] = customer.id

            return redirect('homepage')
        #     else:
        #         error_message = 'Email or Password Invalid'
        else:
            error_message = 'Email or Password Invalid'

        print(email, password)
        return render(request, 'mobile/login.html', {'error': error_message})





def logout(request):
    request.session.clear()
    return redirect('homepage')



class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'mobile/cart.html', {'products': products})

class Checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            order = Order(customer=customer,
                          product=product.id,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(product.id))
            print(order.placeOrder())

        return redirect('cart')


