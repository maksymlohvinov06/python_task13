from django.shortcuts import render, redirect
from .models import Author

def author_list(request):
    authors = Author.objects.all()
    error = request.GET.get('error', '')
    return render(request, 'author/author_list.html', {'authors': authors, 'error': error})

def add_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        patronymic = request.POST.get('patronymic', '')

        if name and surname:
            Author.objects.create(
                name=name,
                surname=surname,
                patronymic=patronymic
            )
        return redirect('author_list')
    return redirect('author_list')

def delete_author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
        if author.books.exists(): 
            return redirect('/authors/?error=Неможливо видалити автора, за яким закріплені книги!')
        author.delete()
    except Author.DoesNotExist:
        pass
    return redirect('author_list')