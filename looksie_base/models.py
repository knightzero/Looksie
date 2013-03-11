from django.db import models
# from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

class Image(models.Model):
    url = models.URLField()
    uuid = models.CharField(max_length=32, unique=True)
    # user = models.ForeignKey(User, default=None, blank=True, null=True)
    views = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add = True)
    session = models.ForeignKey(Session, default=None)
    def __unicode__(self):
        return self.url
    def get_absolute_url(self):
        return reverse('base.views.edit', args=[str(self.uuid)])
    
class Dot(models.Model):
    image = models.ForeignKey('Image', null=True)
    x = models.IntegerField()
    y = models.IntegerField()
    clicks = models.IntegerField()
    title = models.CharField(max_length=255)
    callToAction = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    linkHref = models.URLField()
    linkText = models.CharField(max_length=255)
    uuid = models.CharField(max_length=32, unique=True)