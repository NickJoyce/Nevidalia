from .models import Settings

def company(request):
    return {'settings': Settings.load()}