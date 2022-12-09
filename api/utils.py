from django.urls import reverse

from decouple import config
from django.core.mail import send_mail


#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcwNjA4OTQ5LCJpYXQiOjE2NzA1MjI1NDksImp0aSI6IjczYjIyMjJiYzBmOTQ4Y2Y4MTFmMTNjZjQ3MjcwM2MzIiwidXNlcl9pZCI6MX0.eplm5LBCPMHlwv-biNNEQ-7KbL2bXhu1CtHmRoAhFWE
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



