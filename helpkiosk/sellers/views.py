from django.shortcuts import render
from .models import *

# Create your views here.
def seller_detail(request, pk, *args, **kwargs):
  market = Market.objects.get(pk=pk)
  
  context = {
    'market': market,
  }
  
  return render(request, 'sellers/seller_detail.html', context)