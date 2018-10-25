from django import forms
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy

from .models import Item


def index(request):
    all_item_list = Item.objects.order_by('name')
    context = {
        'all_item_list': all_item_list,
    }
    return render(request,'price/index.html',context)


class DetailView(generic.DetailView):
    model = Item
    template_name = 'price/detail.html'


class PersonCreateView(generic.CreateView):
    model = Item
    template_name = 'price/add.html'
    fields = '__all__'

    initial = {'pub_date': timezone.now()}
    success_url = reverse_lazy('price:index')


class ItemUpdate(generic.UpdateView):
    model = Item
    fields = '__all__'
    template_name = 'price/update.html'
    success_url = reverse_lazy('price:index')


class ItemDelete(generic.DeleteView):
    model = Item
    success_url = reverse_lazy('price:index')


def search_item(request):
    ''' This could be your actual view or a new one '''
    # Your code
    if request.method == 'GET':
        # If the form is submitted
        search_query = request.GET.get('search_box', None)
        all_item_list = Item.objects.filter(name__contains=search_query)
        context = {
            'all_item_list': all_item_list,
        }
        return render (request, 'price/index.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def import_data(request):

    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)


        if form.is_valid():
            request.FILES['file'].save_to_database(
                model=Item,
                mapdicts=[
                    ['name', 'price', 'quantity', 'sold_quantity', 'pub_date']]
            )
            return redirect('price/index')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm ()
        return render (
            request,
            'upload_form.html',
            {
                'form': form,
                'title': 'Import excel data into database example',
                'header': 'Please upload sample-data.xls:'
            })