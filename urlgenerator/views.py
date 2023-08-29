from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from urlgenerator.models import UrlMapping
from django.http import HttpResponse
import string
import random

@login_required(login_url='login')
def home(request):
    # Fetch URL mappings for the current user
    objs = UrlMapping.objects.filter(user=request.user)
    nodes = []
    for obj in objs:
        # Create entry for each URL mapping
        entry = {
            'short_code_link': f'http://127.0.0.1:8000/{obj.short_code}',
            'original_link': obj.original_url,
            'short_cod': obj.short_code,
        }
        nodes.append(entry)
    
    data = {
        'nodes': nodes,
        'short_url': "",
        'short_url_cod':""
    }
    
    if request.method == "POST":
        original_url = request.POST['originalurl']
        existing_mapping = UrlMapping.objects.filter(user=request.user, original_url=original_url).first()
        if existing_mapping:
            short_url = f'http://127.0.0.1:8000/{existing_mapping.short_code}'
            data['short_url'] = short_url
            data['short_url_cod']=existing_mapping.short_code
            return render(request,'home.html',data)
        else:
            # Generate a new short code and create a new URL mapping
            mapping = generate_short_code(request)
            new_url = UrlMapping.objects.create(
                user=request.user, original_url=original_url, short_code=mapping)
            new_url.save()
            short_url = f'http://127.0.0.1:8000/{mapping}'
            data['short_url'] = short_url
            data['short_url_cod']=mapping
            return render(request, 'home.html', data)
    
    data['short_url'] = ""
    return render(request, 'home.html', data)

def generate_short_code(request):
    while True:
        characters = string.ascii_letters + string.digits
        length = 6
        short_code = ''.join(random.choice(characters) for _ in range(length))
        
        # Check if the short code is already in the database
        if not UrlMapping.objects.filter(user=request.user,short_code=short_code).exists():
            return short_code

def redirect_to_original(request, short_code):
    try:
        url_mapping = UrlMapping.objects.get(short_code=short_code)
        return redirect(url_mapping.original_url)
    except UrlMapping.DoesNotExist:
        return HttpResponse("Page not Found sdf")

def deleteLink(request, short_cod):
    try:
        # Delete a URL mapping owned by the user
        urlobj = UrlMapping.objects.get(short_code=short_cod, user=request.user)
        urlobj.delete()
    except:
        pass
    return redirect('home')

def feature(request):
    return render(request,'features.html')