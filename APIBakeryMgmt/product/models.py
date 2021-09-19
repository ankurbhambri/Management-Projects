from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case


class RawMaterial(models.Model):
    item_name = models.CharField(max_length=50)
    avaliable_qty = models.DecimalField(
        max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item_name

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    cost_price = models.FloatField()
    marked_price = models.FloatField()
    discount = models.IntegerField()
    selling_price = models.FloatField()

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if self.discount:
            discount = (self.marked_price * self.discount)/100
            self.selling_price = self.marked_price - discount
            super(Product, self).save(*args, **kwargs)
        else:
            self.selling_price = self.marked_price
            super(Product, self).save(*args, **kwargs)


class Ingredient(models.Model):
    material_name = models.ForeignKey(
        RawMaterial, on_delete=models.CASCADE)
    qty = models.DecimalField(
        max_digits=10, decimal_places=2)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.qty <= self.material_name.avaliable_qty:
            super(Ingredient, self).save(*args, **kwargs)
            self.material_name.avaliable_qty -= self.qty
            self.material_name.save()
        else:
            raise ValidationError(
                'This quantity of raw material is not'
                'avaliable kindly check raw material inventory !')
