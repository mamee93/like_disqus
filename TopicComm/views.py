from django.shortcuts import render,redirect
from .models import Topic,Comments
#from accounts.models import Profile
from .forms import CommentForm
#from django.urls import reverse
# Create your views here.

def all_topic(request):
	all_topic = Topic.objects.all()
	return render(request,'topic/all-list.html',{'all_topic':all_topic})


def topic_details(request,id):
    topic = Topic.objects.get(id=id)
    comments = Comments.objects.filter(topic=topic,parent=None)
    total_comments = comments.count()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            reply_id = request.POST.get('comments_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comments.objects.get(id=reply_id)
            myform.parent=comment_qs
            myform.user = request.user
            myform.topic = topic
            myform.save()
    else:
        form = CommentForm()

    return render(request,'topic/detail.html',{'topic':topic,'comments':comments,'form':form,'total_comments':total_comments})

