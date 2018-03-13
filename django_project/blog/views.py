from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse, redirect
from .models import Author, Tag, Category, Post
from django.contrib import messages
from .forms import FeedbackForm
from django.core.mail import mail_admins
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_project import helpers

def index(request):
    return HttpResponse("Hello Django")


def post_list(request):
    posts = Post.objects.order_by("-id").all()
    posts = helpers.pg_records(request, posts, 5)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk, post_slug):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = get_list_or_404(Post.objects.order_by("-id"), category=category)
    posts = helpers.pg_records(request, posts, 5)
    context = {
        'category': category,
        'posts': posts
    }
    print(category)
    return render(request, 'blog/post_by_category.html', context)


def post_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = get_list_or_404(Post.objects.order_by("-id"), tags=tag)
    posts = helpers.pg_records(request, posts, 5)
    context = {
        'tag': tag,
        'posts': posts
    }
    return render(request, 'blog/post_by_tag.html', context)


def test_redirect(request):
    c = Category.objects.get(name='java')
    return redirect(c)


def feedback(request):
    if request.method == 'POST':
        f = FeedbackForm(request.POST)
        if f.is_valid():
            name = f.cleaned_data['name']
            sender = f.cleaned_data['email']
            subject = "You have a new Feedback from {}:{}".format(name, sender)
            message = "Subject: {}\n\nMessage: {}".format(
                f.cleaned_data['subject'], f.cleaned_data['message'])
            mail_admins(subject, message)

            f.save()
            messages.add_message(request, messages.INFO, 'Feedback Submitted.')
            return redirect('feedback')
    else:
        f = FeedbackForm()
    return render(request, 'blog/feedback.html', {'form': f})

def test_cookie(request):   
    if not request.COOKIES.get('color'):
        response = HttpResponse("Cookie Set")
        response.set_cookie('color', 'blue')
        return response
    else:
        return HttpResponse("Your favorite color is {0}".format(request.COOKIES['color']))

def track_user(request):
    response = render(request, 'blog/track_user.html')
    if not request.COOKIES.get('visits'):
        
        response.set_cookie('visits', '1', 3600 * 24 * 365 * 2)
    else:
        visits = int(request.COOKIES.get('visits', '1')) + 1
        response.set_cookie('visits', str(visits),  3600 * 24 * 365 * 2)
    return response

def stop_tracking(request):
    if request.COOKIES.get('visits'):
       response = HttpResponse("Cookies Cleared")
       response.delete_cookie("visits")
    else:
        response = HttpResponse("We are not tracking you.")
    return response

def test_session(request):
    request.session.set_test_cookie()
    return HttpResponse("Testing session cookie")


def test_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("Cookie test passed")
    else:
        response = HttpResponse("Cookie test failed")
    return response

def save_session_data(request):
    # set new data
    request.session['id'] = 1
    request.session['name'] = 'root'
    request.session['password'] = 'rootpass'
    return HttpResponse("Session Data Saved")


def access_session_data(request):
    response = ""
    if request.session.get('id'):
        response += "Id : {0} <br>".format(request.session.get('id'))
    if request.session.get('name'):
        response += "Name : {0} <br>".format(request.session.get('name'))
    if request.session.get('password'):
        response += "Password : {0} <br>".format(request.session.get('password'))

    if not response:
        return HttpResponse("No session data")
    else:
        return HttpResponse(response)


def delete_session_data(request):
    try:
        del request.session['id']
        del request.session['name']
        del request.session['password']
    except KeyError:
        pass

    return HttpResponse("Session Data cleared")