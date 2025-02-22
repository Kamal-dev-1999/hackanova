from django.shortcuts import render
from googletrans import Translator
from webapp.models import Summary

def translator(request, summary_id):
    summary = Summary.objects.get(id=int(summary_id))
    # Default context: show original text; no translation yet
    context = {
        'summary_id': summary_id,
        'summary_text': summary.summary_text,
        'summary_words': summary.summary_words,
        'duration': summary.duration,
        'title': summary.title,
        'translated': False,  # flag to indicate whether translation has been done
    }
    
    if request.method == 'POST':
        # Get the destination language from the form (default to Hindi "hi")
        destination = request.POST.get('language', 'hi')
        translator_instance = Translator()
        summary_text = summary.summary_text
        lines = summary_text.splitlines()
        translated_lines = []
        
        for line in lines:
            # Detect the language for each line
            result = translator_instance.detect(line)
            # Translate if the line is not already in the destination language
            if result.lang != destination:
                out = translator_instance.translate(line, dest=destination)
                translated_lines.append(out.text)
            else:
                translated_lines.append(line)
        
        translated_text = "\n".join(translated_lines)
        # Update the context with the translated text and flag
        context['out'] = translated_text
        context['translated'] = True
    
    return render(request, 'translate.html', context)


def tt(request, summary_id):
    summary=Summary.objects.get(id=summary_id)
    context = {
    'summary_id': summary_id,
    'summary_text': summary.summary_text,
    'summary_words': summary.summary_words,
    'duration': summary.duration,
    'title': summary.title,
    'transcript_words': summary.transcript_words,
    }
    return render (request, 'translate.html', context)