from django.shortcuts import render

# Create your views here.
def chats(request):
    return render(
        request=request,
        template_name='chats/chats.html',
        context={
            'app_name': 'Chats',
        }
    )