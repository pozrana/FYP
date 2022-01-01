from django.db import models
#from django's db package importing models module

#Model class stores, read and delete the database which is redy
#configure in model class so FoodMenu inherit the common characteristics
#hat belongs to Model class
class FoodMenu(models.Model):
    img = models.ImageField(upload_to = 'pics')
    item_name = models.CharField(max_length = 100)
    price = models.IntegerField()
    desc = models.TextField()


    def __str__(self) -> str:
        return self.item_name