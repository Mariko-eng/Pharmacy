from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.exceptions import ValidationError
from user.models import EmailLog

def send_company_approval_email(email, activation_code, redirect_url):
    recipient_list = [email]  # Assuming you have an 'email' field in your model
    context = {
        "title": "Account Activation Email!",
        'main_message': f'Your company account has been approved, Your activation a code is {activation_code} .',
        'sub_message': 'Your can now validate yourr company account and the create your super user account!',
        'redirect_url': redirect_url,
        }
    subject = 'Account Activation Email!'
    message = strip_tags(render_to_string('company/application/mail/index.html', context=context))

    try:
        send_mail(
            subject= subject,
            message=message,
            from_email= settings.EMAIL_HOST_USER,
            recipient_list= recipient_list,
            fail_silently=False,
            html_message=render_to_string('company/application/mail/index.html', context=context)
        )
        print("Email sent successfully.")
        status = 'Success'
    except ValidationError as e:
        print(f"Validation Error: {e}")
        status = 'Validation Error'
        # Handle validation error, e.g., invalid email address
    except Exception as e:
        print(f"Error sending email: {e}")
        status = 'Error'
    
    # Log the email in the database
    EmailLog.objects.create(subject=subject, recipient=email, status=status)