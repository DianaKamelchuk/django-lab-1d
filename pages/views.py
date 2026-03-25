from django.shortcuts import render

def main_page(request):
    
    context = {
        'title': 'Головна сторінка',
        'pages': ['about', 'contacts', 'services'],
        'is_main': True
    }
    return render(request, 'pages/home.html', context)


def dynamic_page(request, page_id):
   
    context = {
        'title': f'Сторінка: {page_id}',
        'content': f'Ви переглядаєте розділ {page_id}.',
        'is_main': False
    }
    return render(request, 'pages/home.html', context)