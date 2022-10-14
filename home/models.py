from django.db import models
import uuid
from django.contrib.auth.models import User

class ImageModel(models.Model):
    img = models.ImageField(upload_to="images")
    name = models.CharField(max_length=250)
    def __str__(self):
        return f"{self.name}"

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

class Home(models.Model):
    name = models.CharField(max_length=250)
    price = models.FloatField()
    images = models.ManyToManyField(ImageModel)
    description = models.TextField()
    location = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()
    is_active = models.BooleanField(default=True,null=True,blank=True)
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    def save(self,*args,**kwargs):
        self.slug = str(uuid.uuid4())
        super().save(*args,**kwargs)
