from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ContactMessageForm, NewsletterForm
from .models import Newsletter

def contact_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully. We will get back to you soon.")
            return redirect('contacts:contact_page')
        else:
            messages.error(request, "Please check the form fields and try again.")
    else:
        form = ContactMessageForm()
    return render(request, 'contacts/contact.html', {'form': form})

@require_POST
def newsletter_subscribe(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        if Newsletter.objects.filter(email=email).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'You are already subscribed to our newsletter!'})
            messages.warning(request, "You are already subscribed to our newsletter!")
        else:
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Thank you for subscribing to our newsletter!'})
            messages.success(request, "Thank you for subscribing to our newsletter!")
    else:
        errors = form.errors.get('email', ['Invalid email.'])[0]
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': errors})
        messages.error(request, errors)
        
    return redirect('products:home')
