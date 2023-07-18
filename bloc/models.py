from django.db import models
from users.models import CustomUser

class Bloc(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocs', blank=True, null=True)

    def __str__(self):
        return '{0},{1},{2}'.format(self.id, self.description, self.url)


