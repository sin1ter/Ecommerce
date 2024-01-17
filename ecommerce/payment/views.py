from django.shortcuts import render

from . models import ShippingAddress, Order, OrderItem  

from cart.cart import Cart

from django.http import JsonResponse


def checkout(request):
    
    # Users with account -- Pre-fill the form
    
    if request.user.is_authenticated:
        
        try:
            
            # Authenticated users with shipping information
            
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            
            context = {'shipping': shipping_address}
            
            return render(request, 'payment/checkout.html', context=context)
        
        except:
            
            # Authenticated users with no shipping information
            
            return render(request, 'payment/checkout.html')
        
    # Guest users
    
    else: 
        
        return render(request, 'payment/checkout.html')


def complete_order(request):
    
    if request.POST.get('action') == 'post':
        
        name = request.POST['name']  
        email = request.POST['email']
        
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        
        # All-in-one shipping address
        
        shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zipcode)
        
        # Shopping cart information
        
        cart = Cart(request)
        
        # Get the total price of items
        
        total_cost = cart.get_total()
        
        '''

            Order variations
            
            1) Create order -> Account users with + without shippng information
            
            2) Create order -> Guest users without an account
        
        '''
        # 1) Create order -> Account users with + without shippng information
        
        if request.user.is_authenticated:
            
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, 
                                         amount_paid=total_cost,user=request.user)
            
            order_id = order.pk
            
            for item in cart:
                
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                         
                price=item['price'], user=request.user) 
        
        # 2) Create order -> Guest users without an account
        
        else:
                         
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost)
            
            order_id = order.pk
            
            for item in cart:
                
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                        
                price=item['price']) 
        
        order_success = True
        
        response = JsonResponse({'success':order_success})        
        
        return response
            
        
def payment_success(request):
    
    # Clear shopping cart
    
    for key in list(request.session.keys()):
        
        if key == 'session_key':
            
            del request.session[key]
    
    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    
    return render(request, 'payment/payment-failed.html')


