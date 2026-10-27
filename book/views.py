from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Book

def book_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        books = Book.objects.filter(name__icontains=search_query)
    else:
        books = Book.objects.all()
        
    return render(request, 'book/index.html', {'books': books, 'search_query': search_query})

def book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('/') 

    return render(request, 'book/book_detail.html', {'book': book})