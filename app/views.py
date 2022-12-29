from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import ImportForm
import csv,io
from . models import Product


# Create your views here.
# def home(request):
#     return render(request,'upload_csv.html')


def upload_csv(request):
    data = Product.objects.all()
    prompt = {
        'order': 'name,price,description',
        'profiles': data 
    }
    if request.method == "GET":
        return render(request, 'upload_csv.html', prompt)
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        Product.objects.update_or_create(
        name=column[0],
        price=column[1],
        description=column[2]
       
    )
    context = {}

    # if request.method == 'POST':
    #     form = ImportForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         csv_file = request.FILES['csv_file']
    #         print(csv_file)
    #         # list(csv.reader(urllib.request.urlopen(url).read().decode()))
    #         reader = csv.reader(csv_file.read().decode())
    #         print("sssssssss",reader)
    #         for row in reader:
    #             print("row",row)
    #             product = Product()
    #             product.name = row['name']
    #             product.price = row['price']
    #             product.description = row['description']
    #             product.save()
    #         return redirect('home')
    # else:
    #     form = ImportForm()
    return render(request, 'upload_csv.html', {'form': context})
