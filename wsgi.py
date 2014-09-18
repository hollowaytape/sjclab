import os, sys    
sys.path.append(' /Users/Antpile/Code/Baros')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baros.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())