from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from blog.models import Post
from django.views.generic import ListView
from taggit.models import Tag
# Create your views here.

class PostListView(ListView):
    model = Post
    paginate_by = 2
def post_list_view(request,tag_slug=None):
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list,2)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{"post_list":post_list})


from blog.forms import CommentForm
def post_detail_view(request,year,month,day,post):
    post = get_object_or_404(Post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment_form = form.save(commit=False)
            new_comment_form.post = post
            new_comment_form.save()
            csubmit = True
    else:
        form = CommentForm()
    return render(request,'blog/post_detail.html',{"post":post,"form":form,"csubmit":csubmit,"comments":comments})


from blog.forms import EmailSendForm
from django.core.mail import send_mail
def mail_send_view(request,id):
    post = get_object_or_404(Post,id=id)
    sent = False
    if request.method == "POST":
        form = EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            sub = "Subject to mail"
            message = post.body
            send_mail(sub,message,"vaishnavreader97@protonmail.com",[cd['to']])
            sent = True
    else:
        form = EmailSendForm()
    return render(request,"blog/sharebyemail.html",{"form":form,"post":post,"sent":sent})
