from django.shortcuts import render, get_object_or_404
from .models import Blog, Comment
from django.core.paginator import Paginator
from taggit.models import Tag
from django.db.models import Q
from django.core.mail import send_mail
from .forms import CommentForm, EmailPostForm, SignUpForm, ShareBlogForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import redirect



def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/sign_up.html', {'form': form})




def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at') 
    paginator = Paginator(blogs, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = ShareBlogForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            recipient_email = form.cleaned_data['to']
            comment = form.cleaned_data['comment']
            
           
            subject = f"Check out this blog: {blog.title}"
            message = f"Hi,\n\n{name} ({email}) wants to share this blog with you:\n\n{blog.title}\n\n{blog.get_absolute_url()}\n\nComment: {comment}"
            send_mail(subject, message, email, [recipient_email])
            
            
            return redirect('blog_detail', blog_id=blog_id)
    else:
        form = ShareBlogForm()

    

    context = {
        'blog': blog,
        'form': form,
        
    }
    return render(request, 'blog/blog_detail.html', context)
def blog_search(request):
    query = request.GET.get('query')
    results = Blog.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
    
    return render(request, 'blog/blog_search.html', {'results': results, 'query': query})

def blog_share(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    sent = False

    if request.method == 'POST':
        sent = True

    return render(request, 'blog/blog_share.html', {'blog': blog, 'sent': sent})

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    comments = blog.comments.all()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/blog_detail.html', {'blog': blog, 'comments': comments, 'comment_form': comment_form, 'new_comment': new_comment})

def blog_share(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            blog_url = request.build_absolute_uri(blog.get_absolute_url())
            subject = f"{cd['name']} recommends you read '{blog.title}'"
            message = f"Read '{blog.title}' at {blog_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/blog_share.html', {'blog': blog, 'form': form, 'sent': sent})

def custom_logout(request):
    logout(request)
    return redirect('/')