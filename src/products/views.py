from django.db.models import Q
from django.http import Http404
# to create list of products
# to creat detail view of each product

from django.http import Http404

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.utils import timezone



# Create your views here.
#Class based View

# to create list of products
class ProductListView(ListView):
	model = Product
	queryset = Product.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get('q')
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView,self).get_queryset(*args, **kwargs)
		query = self.request.GET.get('q')
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query)|
				Q(description__icontains=query)
				
				)
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs

# to creat detail view of each product
class ProductDetailView(DetailView):
	model = Product
	#template_name = "product.html"
	#template_name = "<appname>/<modelname>_detail.html"


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


