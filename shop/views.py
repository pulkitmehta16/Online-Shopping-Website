from django.shortcuts import render
from django.http import HttpResponse
from .models import product,Contact
from math import ceil

def index(request):
    allprods = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nslides = ceil(n / 4)
        # Split products into chunks of 4
        slides = [prod[i*4:(i+1)*4] for i in range(nslides)]
        # ✅ yahan slides bhejna hai, na ki poora prod
        allprods.append([slides, range(1, nslides+1), nslides])

    para = {'allprods': allprods}
    return render(request, "shop/index.html", para)

def about(request):
    return render(request,'shop/about.html')
def contact(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        subject=request.POST.get('subject','')
        message=request.POST.get('message','')
        contact=Contact(name=name, email=email, subject=subject, message=message)
        contact.save()
    return render(request,'shop/contact.html')
def tracker(request):
    return render(request,'shop/tracker.html')
def search(request):
    return render(request,'shop/search.html')
def prodview(request, myid):
    # fetch product using id
    prodview = product.objects.filter(id=myid)
    return render(request,'shop/prod.html',{'product':prodview[0]})
def checkout(request):
    return render(request,'shop/checkout.html')
