from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from apps.permissions.models import CustomUser

class UserLog(models.Model):
    ACTION_TYPE_CREATE = 1
    ACTION_TYPE_UPDATE = 2
    ACTION_TYPE_DELETE = 3
    ACTION_TYPE_CHOICES = (
        (ACTION_TYPE_CREATE, u'created'),
        (ACTION_TYPE_UPDATE, u'updated'),
        (ACTION_TYPE_DELETE, u'deleted'),
    )

    id = models.BigAutoField(primary_key=True, editable=False)

    object_id = models.PositiveIntegerField(
        verbose_name=u'object ID',
        blank=True,
        null=True,
    )

    app_name = models.CharField(
        verbose_name=u'application name',
        max_length=30,
    )

    model_name = models.CharField(
        verbose_name=u'model name',
        max_length=30,
    )

    action = models.PositiveSmallIntegerField(
        verbose_name=u'action',
        choices=ACTION_TYPE_CHOICES,
    )

    object_instance = models.TextField(
        default="[]",
        verbose_name=u'object values after the action',
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=u'user who made the action',on_delete=models.CASCADE
    )

    ip = models.GenericIPAddressField(
        verbose_name=u'IP',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        verbose_name=u'date and time when the changes were made',
        default=timezone.now,
    )

    def get_model_name(self):
        content_type = ContentType.objects.get(
            app_label=self.app_name,
            model=self.model_name,
        )
        return content_type.model_class()._meta.verbose_name.title()
    get_model_name.short_description = u'Model verbose name'

    class Meta:
        verbose_name = 'User Log'
        verbose_name_plural = 'User Log'
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'{0}.{1}'.format(self.app_name, self.model_name)

    def __eq__(self,obj):
        for key in self.__dict__.keys():
            if key not in ['id','created_at','_state']:
                print(self.__dict__[key],obj.__dict__[key])
                if not self.__dict__[key] == obj.__dict__[key]:
                    return False
            elif key == 'created_at': 
                if((obj.__dict__[key]-self.__dict__[key]).seconds > 50):
                    print('left time')
                    print((obj.__dict__[key]-self.__dict__[key]).seconds)
                    return False
            elif key == 'fields':
                for field_key in self.__dict__[key].keys():
                    if field_key not in ['created_At']:
                        if not obj.__dict__[key][field_key] == self.__dict__[key][field_key]:
                            return False
        return True