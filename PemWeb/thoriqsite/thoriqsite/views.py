from django.shortcuts import render

def welcome(request):
    template_name = 'index.html'
    context = {
        'title': 'Welcome to ThoriqSite',
    }   
    return render(request, template_name, context)