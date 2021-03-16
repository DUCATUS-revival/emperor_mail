from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import send_mail
from django.core.mail import get_connection
from django.core.mail import send_mail
from emperor.settings import EMAIL_HOST, EMPEROR_HOST_USER, EMPEROR_HOST_PASSWORD, EMPEROR_MAIL, EMAIL_PORT, EMAIL_USE_TLS


def get_emperor_mail_connection():
    return get_connection(
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMPEROR_HOST_USER,
        password=EMPEROR_HOST_PASSWORD,
        use_tls=EMAIL_USE_TLS,
    )


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)

@api_view(http_method_names=['POST'])
def emperor_contact_us(request):
    '''
    view for contact us form
    '''
    request_data = request.data
    name = request_data.get('name')
    email = request_data.get('email')
    phone = request_data.get('phone')
    message = request_data.get('message')

    connection = get_emperor_mail_connection()
    text = """
                Name: {name}
                E-mail: {email}
                Message: {message}
                Phone: {phone}
                """.format(
        name=name, email=email, phone=phone, message=message
    )
    send_mail(
        'Request from emperor-holdings contact form',
        text,
        EMPEROR_HOST_USER,
        [EMPEROR_MAIL],
        connection=connection,
    )
    print('message sent')
    return Response('OK', status=status.HTTP_200_OK)

