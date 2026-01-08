from django.contrib import admin

from .models import product
from .models import Contact

admin.site.register(product)
admin.site.register(Contact)
