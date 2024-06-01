from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import TemplateResponseMixin
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Product, ScanHistory, ChatMessage, Post
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'  
    context_object_name = 'products'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy('myproject:product_list')  



class ProductSearchView(ListView):
    model = Product
    template_name = 'search_product.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Product.objects.filter(name__icontains=query) | Product.objects.filter(barcode__icontains=query)
        else:
            return Product.objects.all()[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context



class CheckProductView(TemplateResponseMixin, View):
    template_name = 'check_product.html'

    def get(self, request, *args, **kwargs):
        barcode = request.GET.get('barcode')
        if not barcode:
            return self.render_to_response({})
        
        try:
            product = Product.objects.get(barcode=barcode)
            # Если продукт найден, проверяем его статус верификации
            if product.verified:
                response = {
                    'success': True,
                    'message': f"Product '{product.name}' is verified.",
                    'product_name': product.name,
                    'verified': product.verified
                }
            else:
                response = {
                    'success': False,
                    'message': "Product found but not verified.",
                    'product_name': product.name,
                    'verified': product.verified
                }
        except Product.DoesNotExist:
            response = {'success': False, 'message': 'Product not found.'}

        return render(request, 'verifing_result.html', {'response': response})

class IndexListView(ListView):
    model = ScanHistory
    template_name = 'index.html'
    context_object_name = 'histories'

class BlogListView(ListView):
    model = Post
    template_name = 'blog_list.html'
    context_object_name = 'blogs'


from openai import OpenAI
key = 'sk-proj-Rd2kVMui6J29EL1cVSxxT3BlbkFJE8g23TTYFdUP8qHMl1tO'

client = OpenAI(api_key=key)

def chat(request):
    if request.method == "POST":
        user_message = request.POST.get('message', '')
        # Save user message to the database
        ChatMessage.objects.create(user=request.user, text=user_message, is_gpt=False)

        # Generate AI response
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=user_message,
            temperature=0.7,
            max_tokens=400
        )
        ai_message = response.choices[0].text.strip() if response.choices else "Sorry, I couldn't understand that."

        # Save AI message to the database
        ChatMessage.objects.create(user=request.user, text=ai_message, is_gpt=True)

        return JsonResponse({'user_message': user_message, 'ai_message': ai_message})
    chats = ChatMessage.objects.filter(user=request.user)
    return render(request, 'chat.html', {'chats': chats})

from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import CommentForm

class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('myproject:post_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('myproject:profile_view')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('myproject:index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

