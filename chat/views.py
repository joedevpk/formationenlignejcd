from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message
from django.http import JsonResponse
from django.contrib.auth.models import User
import mimetypes


User = get_user_model()



@login_required
def upload_file(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    file = request.FILES.get("file")
    receiver_id = request.POST.get("receiver_id")

    if not file or not receiver_id:
        return JsonResponse({"error": "missing data"}, status=400)

    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "user not found"}, status=404)

    # 💾 SAVE MESSAGE
    msg = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        file=file
    )

    # 🔥 SAFE FILE TYPE DETECTION
    file_type = file.content_type or mimetypes.guess_type(file.name)[0]

    return JsonResponse({
        "file_url": msg.file.url,
        "file_type": file_type or "file",
        "message_id": msg.id
    }) 


def detect_file_type(filename):
    if filename.endswith((".mp3", ".webm", ".wav")):
        return "audio"
    if filename.endswith((".jpg", ".jpeg", ".png")):
        return "image"
    return "file"

@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return redirect('chat_list')

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    return render(request, "chat/chat.html", {
        "other_user": other_user,
        "messages": messages
    })


@login_required
def conversations(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/conversations.html', {'users': users})