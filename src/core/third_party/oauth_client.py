from ..config import settings
from authlib.integrations.starlette_client import OAuth

google_auth = OAuth()

def init_google():
    global google_auth 
    google_auth.register(
    name='google',
    client_id=settings.CLIENT_ID,       
    client_secret=settings.CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile' 
    }
)