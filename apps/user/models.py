from apps.reviewer.models import Reviewer
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from apps.permissions.models import CustomUser
from apps.admin_user.models import Category
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

STATUS_UNSUBMITTED = 'Unsubmitted'
STATUS_UNDER_REVIEW = 'Under Review'
STATUS_REJECTED = 'Rejected'
STATUS_ACCEPTED = 'Accepted'
STATUS_REVIEWER_PUBLISHED = 'Reviewer Published' #publish to admin
STATUS_ADMIN_PUBLISHED = 'Admin Published'
STATUS_CHOICES = [
    (STATUS_UNSUBMITTED, 'Unsubmitted'),
    (STATUS_UNDER_REVIEW, 'Peer Review'),
    (STATUS_REJECTED, 'Rejected'),
    (STATUS_ACCEPTED, 'Accepted'),
    (STATUS_REVIEWER_PUBLISHED, 'Reviewer Published'),
    (STATUS_ADMIN_PUBLISHED, 'Admin Published'),
]



class NormalUser(models.Model):
    
    gender_choice = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Third Gender', 'Third Gender')
)

    # institution
    # department
    # bio
    
    normal_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length = 250)
    email = models.EmailField()
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=gender_choice, default='Male', blank=True)
    contact = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tbl_normal_user'
        verbose_name = _("normal_user")
        verbose_name_plural = _("normal_user")
        permissions = (
            ("normal_user_view_by_reviewer", "Can View Normal User of Reviewer Part"),
         
        )

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
def validate_imagesize(image):
    file_size = image.file.size
    limit_kb = 500
    if file_size > limit_kb * 1024:
        raise ValidationError("Max Size of file is %s KB" % limit_kb)

def file_size(value): 
    file_size = value.size
    limit_kb = 10000
    if file_size > limit_kb*1024:
        raise ValidationError("Max Size of file is %s KB" % limit_kb)

class Article(models.Model):
    title = models.CharField(max_length=250, null = True)
    file = models.FileField(upload_to='Journal_papers', null=True,  validators=[FileExtensionValidator( ['pdf']), file_size])
    file_image = models.ImageField(upload_to='Journal_Papers_image', null=True,blank=True, validators=[FileExtensionValidator( ['jpg', 'png', 'jpeg']), validate_imagesize])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank = True)
    new_category = models.CharField(help_text = 'Only add new Category if you do not see your wise category in Category Choice list.',
                                    max_length=100,null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    description = RichTextField(null=True, blank=True)
    # description = CKEditor5Field('Description', config_name='extends', null=True, blank=True)
    meta_tags = models.TextField(null=True, blank=True)
    tags = TaggableManager( blank=True)
    views= models.ManyToManyField(CustomUser, related_name='article_views', null=True, blank=True)
    reviewed_by = models.ForeignKey(Reviewer, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'tbl_article'
        verbose_name = _("article")
        verbose_name_plural = _("articles")
        permissions = (
            ("view_publish_articles_to_sites", "Can view published articles to sites"),
            ("publish_articles_to_sites", "Can Published articles to sites"),
              ("article_publish_to_admin_by_reviewer", "Can publish  article to admin"),
                 ("check_article", "Can check  user articles"),
            ("each_article_view", "Can  view each articles "),#for admin sides
            ("view_unpublish_articles", "Can view unPublished articles"),#this is the accepted articles by reviewer which is yet unpublish by admin
    
        )
        
    def averageReview(self):
        reviews = Feedback.objects.filter(article=self).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
   
    def total_views(self):
        return self.views.count()
class Feedback(models.Model):
    status = (
        ('Accepted','Accepted'),('Rejected','Rejected')
    )
    status = models.CharField(max_length=50,choices = status, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(NormalUser,on_delete=models.CASCADE,null=True,blank = True)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)], null=True, blank=True)
    reviewed_by = models.ForeignKey(Reviewer, on_delete=models.CASCADE,null=True, blank=True)
    

    def __str__(self):
        return self.status