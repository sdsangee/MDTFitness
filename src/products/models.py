from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save


#Implementing Query set to get only the products marked as active
class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

#Create Model Managers
class ProductManager(models.Manager):
	def get_querset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return self.get_querset().active()

# Create your models here.
class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	active = models.BooleanField(default=True)
	#slug
	#inventory?
	objects = ProductManager()
	def __unicode__(self):
		return self.title
	def get_absolute_url(self):
		return reverse("product_detail", kwargs={"pk":self.pk})
		#works just fine
		#return "/products/%s"%(self.pk)
		


# Product images
# Product Category
class Variation(models.Model):
	product = models.ForeignKey(Product)
	title = models.CharField(max_length=120)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True) 

	def __unicode__(self):
		return self.title
	
	def get_price(self):
		if self.sale_price is not None:
			return self.sale_price
		else:
			return self.price

	def get_absolute_url(self):
		return self.product.get_absolute_url()		

#fucntion to get notified about a product being saved using post_save_signal
def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
	#print sender
	product = instance
	variations = product.variation_set.all()
	if variations.count() == 0:
		new_var = Variation()
		new_var.product = product
		new_var.title = "Default"
		new_var_price = product.price
		new_var.save()
	

post_save.connect(product_post_saved_receiver, sender=Product)				
		
#Product Images		

class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to='products/')

	def __unicode__(self):
		return self.product.title


