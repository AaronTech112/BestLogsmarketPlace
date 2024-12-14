from .views import get_cart_item_count

def cart_item_count(request):
    # Return the cart item count for the template
    return {
        'cart_item_count': get_cart_item_count(request)
    }
