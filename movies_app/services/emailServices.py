from django.core.mail import send_mail
from django.conf import settings

endpoint = f'https://{settings.HOST_NAME}/users/confirm/'


def generate_confirmation_url(user_id, code):
    return endpoint + str(user_id) + '/' + str(code)


def send_confirmation_url(user, code):
    confirmation_url = generate_confirmation_url(user.id, code)
    user_email = user.email

    send_mail(
        'Confirm your account on MovieHunter',
        '',
        settings.EMAIL_HOST_USER,
        [user_email],
        html_message=f"""<div>Thanks for signing up with MovieHunter! Please confirm your email address: <a href="{confirmation_url}"> confirm </a> </div>"""
    )