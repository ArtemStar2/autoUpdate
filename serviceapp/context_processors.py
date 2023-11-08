from service.models import Service, SocialNetwork
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.models import User
from balances.models import UserBalance
from users.models import Channel
from orders.models import PhraseGroup

def system(request):
    access_token = None
    refresh_token = None
    access_token = request.COOKIES.get('access')
    current_url = request.path
    
    try:
        token = AccessToken(access_token)
        if token.is_expired():
            print(access_token)
    except Exception as e:
        print(e)
        refresh_token = request.COOKIES.get('refresh')
        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)

    if(token.payload.get('user_id')):
        user = User.objects.get(id=token.payload.get('user_id'))
        user_balance, created = UserBalance.objects.get_or_create(user=user)
        channels = Channel.objects.filter(user=user)
    
    many = None
    if(token.payload.get('user_id')):
        if(user_balance):
            many = round(user_balance.balance)
    
    if(token.payload.get('user_id')):
        system = {
            'site_title': 'Мой сайт',
            'logo_url': '/static/images/logo.png',
            'cookie_access' : access_token,
            'user' : user,
            'balance' : many,
            'current_url' : current_url,
            'channels_user' : channels,
        }
    else:
        system = {
            'site_title': 'Мой сайт',
            'logo_url': '/static/images/logo.png',
            'cookie_access' : "",
            'current_url' : current_url,
        }
        
    return {'system': system}
    # return response

def service(request):
    services = Service.objects.all()
    socials = SocialNetwork.objects.all()
    Phrase = PhraseGroup.objects.all()
    
    service = {
        'services': services,
        'socials' : socials,
        'PhraseGroup' : Phrase
    }
    return {'service': service}