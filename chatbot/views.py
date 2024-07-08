import os
from django.shortcuts import render
from django.http import JsonResponse
from .chat_with_docs import configure_retrieval_chain

# Get current dir
current_dir = os.path.dirname(os.path.abspath(__file__))

# Initial PDF setup
temp_dir = os.path.join(current_dir, 'raw-pdfs', 'board-games', 'Cuba Rules.pdf')
CONV_CHAIN = configure_retrieval_chain(temp_dir)

def chatbot(request):
    global CONV_CHAIN
    if request.method == 'POST':
        message = request.POST.get('message')
        response = CONV_CHAIN.run({"question": message})
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')

def load_pdfs(request, category):
    base_dir = os.path.join(current_dir, 'raw-pdfs', category)
    pdfs = [f for f in os.listdir(base_dir) if f.endswith('.pdf')]
    return JsonResponse({'pdfs': pdfs})

def select_pdf(request):
    global CONV_CHAIN
    if request.method == 'POST':
        pdf_path = request.POST.get('pdf_path')
        full_pdf_path = os.path.join(current_dir, 'raw-pdfs', pdf_path)
        if os.path.exists(full_pdf_path):
            CONV_CHAIN = configure_retrieval_chain(full_pdf_path)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed', 'error': 'File not found'})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request method'})
