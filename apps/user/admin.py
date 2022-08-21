from apps.permissions.models import CustomUser
from apps.user.models import Article, NormalUser, Feedback
from django.contrib import admin

# Register your models here.
admin.site.register(NormalUser)
admin.site.register(CustomUser)
admin.site.register(Article)
admin.site.register(Feedback)


