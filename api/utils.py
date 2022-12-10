from django.urls import reverse

from decouple import config
from django.core.mail import send_mail


def send_invitation_email(email, board):

    text = f"""
    Dear, You are invited to be part of {board.title} project, 
    click the link below to fulfil registration \n
    {config('HOST')}{reverse("register-api")} 
    """

    send_mail(
        subject='Invitation',
        message=text,
        from_email='iswearican.a@gmail.com',
        recipient_list=[email],
        fail_silently=False
    )



