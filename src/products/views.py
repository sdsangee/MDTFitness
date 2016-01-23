from django.http import Http404
# to create list of products
from django.views.generic.list import ListView
# to creat detail view of each product
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from .models import Product


# Create your views here.
#Class based View

# to create list of products
class ProductListView(ListView):
	model = Product

# to creat detail view of each product
class ProductDetailView(DetailView):
	model = Product
	#template_name = "product.html"
	#template_name = "<appname>/<modelname>_detail.html"

'''	
def product_detail_view_func(request, id):
	#product_instance = Product.objects.get(id=id)
	product_instance = get_object_or_404(Product, id=id)
	try:
		product_instance = Product.objects.get(id=id)
	except Product.DoesNotExist:
		raise Http404
	except:
		raise Http404
	template = "products/product_detail.html"
	context = {
		"object" : product_instance
	}
	return render(request, template, context)

'''
