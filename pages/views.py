from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html', {
        'title': 'Про нас',
        'content': 'Це сторінка про нас'
    })

def contacts(request):
    return render(request, 'pages/contacts.html', {
        'title': 'Контакти',
        'content': 'Наші контакти тут'
    })