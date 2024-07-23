import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.http import JsonResponse
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
from .models import Post, Album, Blogpost, UserProfile


def home(request):
    return render(request, 'home.html')


def post_list(request):
    posts = Post.objects.all()  # Query all posts
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})


def album_list(request):
    albums = Album.objects.all()
    return render(request, 'album_list.html', {'albums': albums})


def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    print(album)  # Check album object
    return render(request, 'album_detail.html', {'album': album})


def About(request):
    return render(request, 'About.html')

def Contact(request):
    return render(request, 'Contact.html')

def Blog(request):
    blog_posts = Blogpost.objects.all()
    return render(request, 'Blog.html', {'blog_posts': blog_posts})


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Specify your custom login template path here

    def get_success_url(self):
        return reverse_lazy('admin:index')


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
def process_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')

            charge = stripe.Charge.create(
                amount=5000,  # Amount in cents
                currency='usd',
                description='Example charge',
                source=token,
            )
            return redirect('payment_success')  # Redirect to success page

        except stripe.error.CardError as e:
            # Handle card error
            return redirect('payment_error')  # Redirect to error page

        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            return redirect('payment_error')  # Redirect to error page

        except Exception as e:
            # Handle general errors
            return redirect('payment_error')  # Redirect to error page

    return redirect('payment_error')  # Redirect to error page

def payment_success(request):
    return render(request, 'success.html')

def payment_error(request):
    return render(request, 'error.html')


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_checkout_session(request):
    if request.method == 'GET':
        try:
            # Your session creation code here
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Sample Product',
                            },
                            'unit_amount': 2000,  # Amount in cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/payment-success/'),
                cancel_url=request.build_absolute_uri('/payment-error/'),
            )
            return JsonResponse({'id': session.id})
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=500)
