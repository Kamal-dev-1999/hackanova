from django.shortcuts import redirect, render
from django.views import View
from webapp.models import UserProfile
from webapp.models import Video, Summary

import subprocess
from webapp.models import Video




class Dashboard(View):
     def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        user_profile = UserProfile.objects.get(id=user_id)
        user = user_profile.user
       # summary_id=request.session.get('summary_id')
     #   try:
         #   summary = Summary.objects.get(id=summary_id)
        #except Summary.DoesNotExist:
       #     summary = None
       # summary = summary_view(request, user, page='dashboard')
        videos = Video.objects.order_by('-upload_date')
        summary=Video.objects.order_by('-upload_date')
      #  summaries = Summary.objects.filter(user=user)
       # summary=Summary.objects.get(id=user_id)
      #  userr=Video.objects.get(id=user_id)
      #  videos = Video.objects.filter(user=user)
       # if not videos.exists():
             #  videos = None

        context = {
            'first_name': user_profile.first_name,
            'email': user_profile.email,
            'username': user_profile.username,
            'summary': summary,
            'videos': videos,
        }
        return render(request, 'dashboard.html', context)

from django.shortcuts import render
from webapp.models import Video

class MyVideosView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        user_profile = UserProfile.objects.get(id=user_id)
        user = user_profile.user
        videos = Video.objects.filter(user=user)
        
        if not videos.exists():
            videos = None
        
        context = {
           # 'title': user.title ,
            'videos': videos,
        }
        return render(request, 'storage.html', context)
    
    
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import os

def summary_view(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id)
    # Assuming your summary object has an attribute (or a way to determine) the file name
    file_path = os.path.join(settings.BASE_DIR, f'media/summaries/{summary.title}.txt')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            summary_transcript = f.read()
    except FileNotFoundError:
        summary_transcript = "Summary transcript not found."
    
    context = {
        'summary': summary,
        'summary_transcript': summary_transcript,
    }
    return render(request, 'summary_list.html', context)

