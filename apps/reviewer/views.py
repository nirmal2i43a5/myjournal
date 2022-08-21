from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group
from apps.user.models import NormalUser
from django.contrib.auth.decorators import login_required, permission_required  
from django.contrib import messages
from apps.user.models import Article,Feedback
from apps.user.forms import FeedbackForm
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required






@permission_required('reviewer.add_reviewer', raise_exception=True)
def add_reviewer(request):
    auth_form = CustomUserForm()
    reviewer_user = ReviewerRegisterForm()
    context = {
        'title':'Register',
        'auth_form':auth_form,
        'reviewer_user':reviewer_user
    }
    
    if request.method == 'POST':
        auth_form = CustomUserForm(request.POST,request.FILES)
        reviewer_user = ReviewerRegisterForm(request.POST,request.FILES)
        
        if auth_form.is_valid() and reviewer_user.is_valid():
            
            username = auth_form.cleaned_data["username"]
            
            if request.FILES.get('image'):
                image_url = request.FILES['image']
            else:
                image_url = None
           
            group = Group.objects.get(name = 'Reviewer')
            user = CustomUser.objects.create_user(
                username=username, password="password",
                user_type=group)
        
    
            user.reviewer.full_name = reviewer_user.cleaned_data['full_name']
            user.reviewer.email = reviewer_user.cleaned_data['email']
            user.reviewer.dob = reviewer_user.cleaned_data['dob']
            user.reviewer.gender = reviewer_user.cleaned_data['gender']
            user.reviewer.contact = reviewer_user.cleaned_data['contact']
            user.reviewer.address = reviewer_user.cleaned_data['address']
            if image_url != None:
                user.reviewer.image = image_url
            user.save()
            user.groups.add(group)#adding user to particular group.ie role
            messages.success(request, "Successfully Created Reviewer")
            return redirect('admin_app:reviewer-index')
         
    return render(request,'reviewer/add.html',context)


def edit_reviewer(request,pk):
    rev_instance = get_object_or_404(Reviewer,pk = pk)
    customuser_instance = get_object_or_404(CustomUser, pk = rev_instance.reviewer_user.pk)
    auth_form = CustomUserForm(instance=customuser_instance)
    reviewer_form = ReviewerRegisterForm(instance = rev_instance)
    
    if request.method == "POST":
        auth_form = CustomUserForm(request.POST, request.FILES,instance=customuser_instance,)
        reviewer_form = ReviewerRegisterForm(request.POST, request.FILES,instance = rev_instance)
        if auth_form.is_valid() and reviewer_form.is_valid():
            auth_form.save()
            reviewer_form.save()
            messages.success(request, "Successfully Edited Reviewer")
            return redirect('admin_app:reviewer-index')
            
        
    context = {
        'title':'Register',
        'instance':rev_instance,
        'auth_form':auth_form,
        'reviewer_user':reviewer_form
    }
    return render(request,'reviewer/add.html',context)

def delete_reviewer(request,pk):
    customuser_instance = get_object_or_404(CustomUser, pk = pk)
    customuser_instance.delete()
    messages.success(request, "Successfully deleted reviewer")
    return redirect('admin_app:reviewer-index')
            

@permission_required('user.normal_user_view_by_reviewer', raise_exception=True)
def normal_user_index(request):
    users = NormalUser.objects.all()
    total_articles = []
    rejected_articles = []
    accepted_articles = []
    articles_under_review = []
    for user in users:
        user_object = get_object_or_404(CustomUser,id = user.normal_user.id )
        articles = user_object.article_set.all()
        accepted_articles = user_object.article_set.filter(status = STATUS_REVIEWER_PUBLISHED)
        rejected_articles = user_object.article_set.filter(status = STATUS_REJECTED)
        article_under_review = user_object.article_set.filter(status = STATUS_UNDER_REVIEW)
        article_publish_to_admin = user_object.article_set.filter(status = STATUS_ADMIN_PUBLISHED)
        total_articles_count = articles.count()
        accepted_articles_count = accepted_articles.count()
        rejected_articles_count = rejected_articles.count()
        article_under_review_count = article_under_review.count()
        article_publish_to_admin_count = article_publish_to_admin.count()
        print(";::::::::::", article_publish_to_admin_count)
        
        total_articles.append({'total_articles':total_articles_count,'accepted_articles_count':accepted_articles_count,
                               'rejected_articles_count':rejected_articles_count,'article_under_review_count':article_under_review_count,
                               'article_publish_to_admin':article_publish_to_admin_count})
        
    context = {
        'title':'Manage User',
        'users':zip(users,total_articles)
    }
    
    return render(request,'reviewer/manage_user.html',context)



def view_user_under_review_articles(request,pk):
    articles_under_review = Article.objects.filter(status = STATUS_UNDER_REVIEW,user__pk = pk)
    user = get_object_or_404(CustomUser, pk = pk)

    context = {
        'title':'Articles',
        'articles_under_review':articles_under_review,
        # 'articles_review_feedback':zip(articles_under_review,checked_articles),
        # 'checked_articles':checked_articles,
        
    }
    return render(request,'reviewer/articles_under_review.html',context)



def view_user_accepted_articles_list(request,pk):
    accepted_articles = Article.objects.filter(status = STATUS_REVIEWER_PUBLISHED, user__pk = pk)
    user = get_object_or_404(CustomUser, pk = pk)
    # articles = user.article_set.all()
    # checked_articles = []
    # for article in articles:
    #     article_obj = get_object_or_404(Article, pk = article.pk)
    #     article_feedback = article_obj.feedback_set.all()
    #     if article_feedback:
    #         checked_articles.append(article_obj)
            
   
    #
    context = {
        'title':'Accepted Articles',
        'accepted_articles':accepted_articles
        # 'articles_review_feedback':zip(articles_under_review,checked_articles),
        # 'checked_articles':checked_articles,
        
    }
    return render(request,'reviewer/accepted_articles.html',context)


def view_user_rejected_articles(request,pk):
    rejected_articles = Article.objects.filter(status = STATUS_REJECTED,user__pk = pk)
    user = get_object_or_404(CustomUser, pk = pk)
    # articles = user.article_set.all()
    # checked_articles = []
    # for article in articles:
    #     article_obj = get_object_or_404(Article, pk = article.pk)
    #     article_feedback = article_obj.feedback_set.all()
    #     if article_feedback:
    #         checked_articles.append(article_obj)
            
   
    #
    context = {
        'title':'Rejected Articles',
        'rejected_articles':rejected_articles,
        # 'articles_review_feedback':zip(articles_under_review,checked_articles),
        # 'checked_articles':checked_articles,
        
    }
    return render(request,'reviewer/rejected_articles.html',context)


@permission_required('user.check_article', raise_exception=True)
def check_user_article(request,pk):
    article = get_object_or_404(Article, pk = pk)
    context = {
        'title':'Article Check',
        'article':article,
        'form':FeedbackForm()
    }
    return render(request,'reviewer/check-user-article.html',context)

@permission_required('user.check_article', raise_exception=True)
def check_review_accepted_user_article(request,pk):
    article = get_object_or_404(Article, pk = pk)
    context = {
        'title':'Article Check',
        'article':article,
    }
    return render(request,'reviewer/check-reviewer-accepted-user-article.html',context)


@permission_required('user.check_article', raise_exception=True)
def view_accepted_user_article(request,pk):
    article = get_object_or_404(Article, pk = pk)
    context = {
        'title':'Article Check',
        'article':article,
    }
    return render(request,'reviewer/view-accepted-user-article.html',context)

@permission_required('user.add_feedback', raise_exception=True)
def article_feedback(request):
    userId = request.POST['userId']
    articleId = request.POST['articleId']
    feedback = request.POST['feedback']
    status = request.POST['status']
    rating = request.POST.get('rating')
    article_object = get_object_or_404(Article,pk = articleId)
    
    print(userId, articleId, feedback, status, rating)
    # print("ghda::",request.user.reviewer)
    if status == 'Accepted':
        article_object.status = STATUS_REVIEWER_PUBLISHED
        article_object.reviewed_by = request.user.reviewer
        article_object.save()
    elif status == 'Rejected':
        # send emai with annotate pdf
        article_object.status = STATUS_REJECTED
        article_object.reviewed_by = request.user.reviewer

        article_object.save()     
    
    customuser_instance = get_object_or_404(CustomUser, pk = userId)
    user_instance = get_object_or_404(NormalUser, pk = customuser_instance.normaluser.pk)
    feedback = Feedback(feedback = feedback, status = status, rating=rating)
    feedback.user = user_instance
    feedback.reviewed_by = request.user.reviewer
    feedback.article = article_object
    feedback.save()
    
    # For sending email to particular user after feedback
    subject = "Journal Article Feedback"
    feedback_message = feedback.feedback
    context = {
        'message':    feedback_message
    }
    template = get_template('reviewer/send_message.html').render(context)
    email = EmailMessage(
        subject,
        template,
        settings.EMAIL_HOST_USER,  # sender
        [user_instance.email],  # receiver
    )
    file = article_object.file
    # for file in files:
    email.attach(file.name, file.read())
    email.content_subtype = 'html'
    email.send()
    email.fail_silently = False
    messages.success(request,"Successfully Review Paper")
    return redirect('reviewer:user-under-review-articles',userId)

@permission_required('user.article_publish_to_admin_by_reviewer', raise_exception=True)
def publish_to_admin(request,user_id,article_id):
    reviewer_object = get_object_or_404(Reviewer, reviewer_user__pk = request.user.id)
    article = Article.objects.get(pk = article_id)
    article.reviewed_by = reviewer_object
    article.status = STATUS_REVIEWER_PUBLISHED
    article.save()
    messages.success(request,"Article Successfully Published to Admin")
    return redirect('reviewer:user-accepted-articles',user_id)
    
def edit_feedback(request,pk):
    feedback_instance = get_object_or_404(Feedback,pk = pk)
    reviewer_form = FeedbackForm(instance = feedback_instance)
    print("up to here")
    if request.method == "POST":
        status = request.POST.get('status')
        feedback = request.POST.get('feedback')
        rating = request.POST.get('rating')
        reviewed_by = request.user.reviewer
        feedback_instance.status = status
        feedback_instance.feedback = feedback
        print("========", feedback_instance.rating)
        feedback_instance.rating = rating
        feedback_instance.reviewed_by = reviewed_by
        feedback_instance.save()
        feedback_update_status = Article.objects.get(pk=feedback_instance.article.pk)
        if feedback_instance.status == 'Rejected':
            feedback_update_status.status = STATUS_REJECTED
            feedback_update_status.reviewed_by = request.user.reviewer
            feedback_update_status.save()

        if feedback_instance.status == 'Accepted':
            feedback_update_status.status = STATUS_REVIEWER_PUBLISHED
            feedback_update_status.reviewed_by = request.user.reviewer
            feedback_update_status.save()
        messages.success(request, "Successfully Edited feedback")
        return redirect('reviewer:user-accepted-articles',feedback_instance.article.user.pk)
            
    context = {
        'title':'Update Feedback',
        'form':reviewer_form,
        'article': feedback_instance.article,
        'feedback': feedback_instance
    }
    return render(request,'reviewer/edit_feedback.html',context)