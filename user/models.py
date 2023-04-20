from django.db import models
from django.contrib.auth.models import User

class Box(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='box_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    @property
    def area(self):
        return self.length * self.breadth
    
    @property
    def volume(self):
        return self.length * self.breadth * self.height