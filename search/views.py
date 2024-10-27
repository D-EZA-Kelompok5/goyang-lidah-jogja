from django.shortcuts import render

# Create your views here.
# search/views.py
from django.shortcuts import render
from .search_engine.engine import MenuSearchEngine

def search_results(request):
    query = request.GET.get('q', '')
    
    if query:
        search_engine = MenuSearchEngine()
        results = search_engine.search(query)
    else:
        results = []
    
    context = {
        'query': query,
        'results': results
    }
    
    return render(request, 'search/search_results.html', context)
