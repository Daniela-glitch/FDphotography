import json
import os

import paypalrestsdk
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render


from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from FDphotography import settings
from .models import Post, Album, Blogpost, UserProfile, Slide


def home(request):
    slides = Slide.objects.all()
    print("Slides:", slides)
    return render(request, 'home.html', {'slides': slides})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})


def album_list(request):
    albums = Album.objects.all()
    return render(request, 'album_list.html', {'albums': albums})


def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    print(album)
    return render(request, 'album_detail.html', {'album': album})


def About(request):
    return render(request, 'About.html')

def Contact(request):
    return render(request, 'Contact.html')

def Blog(request):
    blog_posts = Blogpost.objects.all()
    return render(request, 'Blog.html', {'blog_posts': blog_posts})


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('admin:index')



paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


def create_payment(request):
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri('/payment/execute/'),
            "cancel_url": request.build_absolute_uri('/payment/cancel/')
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": post.title,
                    "sku": "item",
                    "price": str(post.price),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(post.price),
                "currency": "USD"
            },
            "description": "Payment for " + post.title
        }]
    })

    if payment.create():
        return redirect(payment.links[1].href)
    else:
        return JsonResponse({'error': payment.error})

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return redirect(f'/payment/success/?payment_id={payment_id}')
    else:
        return redirect('/payment/cancel/')

def cancel_payment(request):
    return render(request, 'payment/cancel.html')

def success_payment(request):
    payment_id = request.GET.get('payment_id')
    post_id = request.GET.get('post_id')

    return render(request, 'payment/success.html', {'post_id': post_id})

def download_image(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    file_path = post.image.path

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{post.title}.jpg"'
            return response
    else:
        return HttpResponse("File not found.", status=404)