from django.db import models

class itemData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    category = models.CharField(max_length=50, null=False)
    brand = models.CharField(max_length=50, null=False)
    image = models.URLField(max_length=300,null=False)

    class Meta:
        db_table = "Item"