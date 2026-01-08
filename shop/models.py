from django.db import models

class product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50, default='')
    price=models.IntegerField(default=0)
    discription=models.CharField(max_length=10000)
    pub_date=models.DateField()
    image=models.ImageField(upload_to='shop/images', default='')

    def __str__(self):
        return self.product_name
    
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50, default='')
    subject=models.CharField(max_length=100, default='')
    message=models.CharField(max_length=10000)
    
    def __str__(self):
        return self.name