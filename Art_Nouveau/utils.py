from django.core.mail import mail_admins
from django.utils.html import strip_tags


def get_ip(request):
    str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if str_lista_ip:
        return str_lista_ip.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')


def send_custom_admin_email(subject, message_body, is_critical_error=False):
    """
    Sends an email to admins in both Text and HTML formats.
    HTML requirements:
    - Subject included in body as red H1.
    - If is_critical_error is True, the body has a red background.
    """

    # Determine styles based on error flag
    container_style = "background-color: red; color: white; padding: 15px;" if is_critical_error else ""

    # Construct HTML manually to ensure specific styling requirements
    html_message = f"""
    <html>
        <body>
            <h1 style="color: red;">{subject}</h1>
            <div style="{container_style}">
                <p>{message_body}</p>
            </div>
        </body>
    </html>
    """

    # Create plain text version by stripping HTML tags
    plain_message = strip_tags(html_message)

    mail_admins(
        subject=subject,
        message=plain_message,
        html_message=html_message
    )