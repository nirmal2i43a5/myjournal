from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required  
from django.contrib import messages
from django.views.generic import DetailView

def user_register(request):
    auth_form = CustomUserForm()
    user_form = UserRegisterForm()
    context = {
        'title':'Register',
        'auth_form':auth_form,
        'user_form':user_form
    }
    if request.method == 'POST':
        auth_form = CustomUserForm(request.POST,request.FILES)
        print(auth_form)
        user_form = UserRegisterForm(request.POST,request.FILES)
        print(user_form)
        
        if auth_form.is_valid() and user_form.is_valid():
            
            username = auth_form.cleaned_data["username"]
            password1 = auth_form.cleaned_data["password1"]
            password2 = auth_form.cleaned_data["password2"]
            print(password1,password2)
            
            if request.FILES.get('image'):
                image_url = request.FILES['image']
            else:
                image_url = None
           
            group = Group.objects.get(name = 'User')
            
            
            if password1 == password2:
                user = CustomUser.objects.create_user(
                    username=username, password=password2,
                    user_type=group)
            
        
                user.normaluser.full_name = user_form.cleaned_data['full_name']
                user.normaluser.email = user_form.cleaned_data['email']
                user.normaluser.dob = user_form.cleaned_data['dob']
                user.normaluser.gender = user_form.cleaned_data['gender']
                user.normaluser.contact = user_form.cleaned_data['contact']
                user.normaluser.address = user_form.cleaned_data['address']

                if image_url != None:
                    user.normaluser.image = image_url

                user.save()
                user.groups.add(group)#adding user to particular group.ie role
                print(user,"-----group----")
                
                    
                messages.success(request, "Successfully Created User")
                return redirect('login')
            else:
                messages.error(request,'Password does not match.Please, check it properly.')
        
    return render(request,'users/registers.html',context)

def upload_article(request):
    form = PaperUploadForm()
    if request.method == 'POST':
        form = PaperUploadForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.status = STATUS_UNDER_REVIEW
            obj.save()
            form.save_m2m()
            messages.success(request, "Article was uploaded successfully. You article will be reviewed and published with in 24 hours. Thank You!")
            return redirect('user:article-under-review')

        else:
            print(form.errors)
            messages.error(request, "File validation didnot match!")
        
    context = {
        'title':'Upload Paper',
        'form':form
    }
    return render(request,'users/paper_upload.html',context)


def article_update_view(request, pk):
    article_instance = get_object_or_404(Article, id=pk)
    form = PaperUploadForm(instance=article_instance)
    if request.method == 'POST':
        form = PaperUploadForm(request.POST, instance=article_instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.status = STATUS_UNDER_REVIEW
            obj.save()
            form.save_m2m()
            messages.success(request, ('Article was updated successfully.'))
            return redirect('user:article-under-review')
        else:
            print("Error Occured::: ",form.errors)
            messages.error(request, "File validation didnot match!")
            return render(request, 'users/paper_upload.html',{'form':form})
    context = {
        'form':form,    
        'title':'Update Paper' ,
        'article': article_instance,
    }
    return render(request,'users/paper_upload.html',context)

def article_delete_view(request, pk):
    article = get_object_or_404(Article, id=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, ('Article was deleted successfully.'))
        return redirect('user:article-under-review')
    context = {
        'title': 'Delete Paper',
        'article':article,
    }
    return render(request,'users/paper_upload.html',context=context)

# This is the article under review 
def article_under_review(request):
    articles = Article.objects.filter(user = request.user)
    articles_under_review = Article.objects.filter(status = STATUS_UNDER_REVIEW,user = request.user)
    context = {
        'title':'View Paper',
        'articles_under_review':articles_under_review,
    }
    
    return render(request,'users/article-under-review.html',context)


def accepted_article_list(request):
    articles = Article.objects.filter(user = request.user)
    accepted_articles = Article.objects.filter(status = STATUS_ADMIN_PUBLISHED, user = request.user)
    accepted_feedback = []
    for article in articles:
        article_obj = get_object_or_404(Article, pk = article.pk)
        article_feedback = article_obj.feedback_set.all()
        for feedback in article_feedback:     
            if feedback.status == 'Accepted':
                accepted_feedback.append(feedback)
           
    
    context = {
        'title':'Accepted Paper',
        'accepted_articles':zip(accepted_articles,accepted_feedback)
    }
    return render(request,'users/accepted_articles.html',context)

def rejected_article_list(request):
    articles = Article.objects.filter(user = request.user)
    rejected_articles = Article.objects.filter(status = STATUS_REJECTED,user = request.user)
    rejected_feedback = []
    for article in articles:
        article_obj = get_object_or_404(Article, pk = article.pk)
        article_feedback = article_obj.feedback_set.all()
        for feedback in article_feedback:     
            if feedback.status == 'Rejected':
                rejected_feedback.append(feedback)
                
    # print(rejected_feedback)
    
    context = {
        'title':'Rejected Paper',
        'rejected_articles':zip(rejected_articles,rejected_feedback),
    }
    return render(request,'users/rejected_articles.html',context)


def article_view(request,pk):
    article = get_object_or_404(Article, pk = pk)
    context = {
        'title':'Upload Paper',
        'article':article
    }
    return render(request,'users/article-view.html',context)

class ArticleDetailView(DetailView):
    model=Article
    template_name='users/article_detail.html'
    def get_context_data(self,*args, **kwargs):
        self.object.views.add(self.request.user)
        context=super().get_context_data(*args, **kwargs)
        context['article']= context.get('object')
        return context

def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk = pk)
    # print(article.views.id, '::::::::')
    article.views.add(request.user)
    article.save()
    context = {
        'title':'Article Detail View',
        'article':article,
        'logged_user': request.user,
    }
    return render(request,'users/article_detail.html',context)