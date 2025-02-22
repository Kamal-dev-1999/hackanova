import spacy
import re
from webapp.models import Summary,Video
from django.shortcuts import render
import os
from django.conf import settings


def action_words(request, video_id):
    video = Video.objects.get(id=video_id)
    nlp = spacy.load("en_core_web_sm")
    file_path = f'media/main/videos/{video.title}.txt'
    keywords = ["task", "complete", "to do", "assignment", "project", "work", "job", "duty", "responsibility",
            "assign", "assigned", "assigning", "delegate", "delegated", "delegating", "direct", "directed", "directing",
            "instruct", "instructed", "instructing", "charge", "charged", "charging", "enjoin", "enjoined", "enjoining",
            "order", "ordered", "ordering", "command", "commanded", "commanding", "tell", "told", "telling",
            "perform", "performed", "performing", "execute", "executed", "executing", "accomplish", "accomplished", "accomplishing",
            "fulfill", "fulfilled", "fulfilling", "follow", "followed", "following", "carry out", "carried out", "carrying out",
            "implement", "implemented", "implementing", "enforce", "enforced", "enforcing", "enact", "enacted", "enacting",
            "can you please", "i need you to", "could you", "please make sure to", "Announced ",
            "don't forget to", "i'm assigning you to", "you're responsible for", "i want you to",
            "it's your duty to", "please ensure that you", "due date"]
    highlight_color = ''

    # read in file and highlight tasks
    highlighted_sentences = set()
    with open(file_path, "r") as f:
        for line in f:
            doc = nlp(line.strip())
            for token in doc:
                # check if token is a task-related keyword
                if re.match("|".join(keywords), token.text, re.IGNORECASE):
                    highlighted_sentence = highlight_color + \
                        token.sent.text.strip()
                    highlighted_sentences.add(highlighted_sentence)
                    break

    # create context dictionary
    context = {
        'video_id': video_id,
        'highlighted_sentences': highlighted_sentences,
        'video': video,
        
    }

    # render template
    return render(request, 'action_words.html', context)

def calculate_summary_ratio(transcript, summary):
    try:
        transcript_words = len(transcript.split())
        summary_words = len(summary.split())
        return round((summary_words / transcript_words) * 100, 1)
    except:
        return 0
    
def show_original_transcript(request, video_id):
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return render(request, 'error.html', {'message': 'Video not found.'})

    # Load transcript from file
    transcript_file_path = os.path.join(settings.BASE_DIR, f'media/main/videos/{video.title}.txt')
    try:
        with open(transcript_file_path, 'r', encoding='utf-8') as f:
            transcript = f.read()
    except FileNotFoundError:
        transcript = "Transcript not found."

    # Handle multiple summaries
    try:
        # Get the most recent summary
        summary_obj = Summary.objects.filter(video=video).latest('generated_date')
        summary = summary_obj.summary_text
    except Summary.DoesNotExist:
        summary = "Summary not available yet."
    except Summary.MultipleObjectsReturned:
        # Handle case where multiple summaries exist
        latest_summary = Summary.objects.filter(video=video).order_by('-generated_date').first()
        summary = latest_summary.summary_text if latest_summary else "Multiple summaries found, could not load."

    # Calculate duration (add this to your Video model if not present)
    duration = video.duration if hasattr(video, 'duration') else "N/A"

    context = {
        'video': video,
        'transcript': transcript,
        'summary': summary,
        'summary_ratio': calculate_summary_ratio(transcript, summary),
        'duration': duration
    }
    
    return render(request, 'show_transcript.html', context)