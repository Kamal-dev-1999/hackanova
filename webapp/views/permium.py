from django.http import HttpResponseForbidden

def premium_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.userprofile.is_premium:
            return HttpResponseForbidden("Premium feature required")
        return view_func(request, *args, **kwargs)
    return wrapper


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import UpgradeForm
from django.shortcuts import get_object_or_404
from ..models import UserProfile

from django.contrib.auth.decorators import login_required
from django.conf import settings  # Import Django settings

@login_required(login_url=settings.LOGIN_URL)
def upgrade_account(request):
    # CORRECTED: Get the user profile for logged-in user
    user_profile = get_object_or_404(UserProfile, user=request.user)  # Remove the extra .get()
    
    if user_profile.is_premium:
        messages.warning(request, "You're already a premium member!")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UpgradeForm(request.POST)
        if form.is_valid():
            # Process payment here (demo only)
            user_profile.is_premium = True
            user_profile.save()
            messages.success(request, "Premium upgrade successful!")
            return redirect('upgrade_success')
    else:
        form = UpgradeForm()

    context = {
        'form': form,
        'remaining_days': 30 - user_profile.transcription_count  # Example usage
    }
    return render(request, 'upgrade.html', context)

@login_required
def upgrade_success(request):
    return render(request, 'upgrade_success.html')