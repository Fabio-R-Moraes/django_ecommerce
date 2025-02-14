from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .signals import object_viewed_signal
from .utils import get_client_ip

User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE) #specificuser, instance.id
    ip_address = models.CharField(max_length=30, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) #Product, OOrder, Cart, Address, etc...
    object_id = models.PositiveIntegerField() #User id, Product id, Order id, etc...
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_object} viewed on {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp'] #most recent saved show up first
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender) #instance.__class__
    new_view_obj = ObjectViewed.objects.create(
        user = request.user,
        content_type = c_type,
        object_id = instance.id,
        ip_address = get_client_ip(request)
    )

    print("="*60)
    print(sender)
    print(instance)
    print(request)
    print(request.user)
    print("="*60)

object_viewed_signal.connect(object_viewed_receiver)