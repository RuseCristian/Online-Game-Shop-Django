import concurrent.futures
from django.shortcuts import render
from django.db.models import Q
from django import forms
from ..models import Category, Products


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)


def search(request):
    form = SearchForm(request.GET or None)
    results = []

    if form.is_valid():
        query = form.cleaned_data.get('query')
        categories = []
        search_keywords = []

        # Parse search query to extract categories and search keywords
        search_terms = query.split()
        for term in search_terms:
            if term.startswith("#"):
                categories.append(term[1:])
            else:
                search_keywords.append(term)

        def search_category(category):
            category_id = Category.objects.filter(name__iexact=category).values_list('id', flat=True).first()
            category_results = Products.objects.filter(category_id=category_id).filter(
                Q(name__icontains=' '.join(search_keywords)) | Q(description__icontains=' '.join(search_keywords))
            )
            return category_results

        if not categories:
            # Perform search across the entire product database by name if no category is specified
            results.extend(Products.objects.filter(
                Q(name__icontains=' '.join(search_keywords)) | Q(description__icontains=' '.join(search_keywords))
            ))
        else:
            # Perform parallel search for each category concurrently using threading
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(search_category, category) for category in categories]
                concurrent_results = [future.result() for future in concurrent.futures.as_completed(futures)]
                results.extend(concurrent_results)

    return render(request, 'index.html', {'form': form, 'results': results})
