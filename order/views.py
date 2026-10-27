from django.shortcuts import render, redirect
from django.utils import timezone
import datetime
from .models import Order
from book.models import Book

def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.user.role == 1:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
        
    return render(request, 'order/order_list.html', {'orders': orders})

def create_order(request, book_id):
    if request.method == 'POST' and request.user.is_authenticated:
        book = Book.objects.get(id=book_id)
        if book.count > 0:
            planned_date = timezone.now() + datetime.timedelta(days=14)
            
            Order.objects.create(
                user=request.user, 
                book=book,
                plated_end_at=planned_date 
            )
            book.count -= 1  
            book.save()
    return redirect('order_list')

def close_order(request, order_id):
    if request.method == 'POST' and request.user.is_authenticated and request.user.role == 1:
        try:
            order = Order.objects.get(id=order_id)
            book = order.book
            book.count += 1  
            book.save()
            order.delete()   
        except Order.DoesNotExist:
            pass
    return redirect('order_list')