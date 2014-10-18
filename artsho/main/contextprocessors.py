from .models import Show


def menu_items(request):
    return {
        'all_shows': Show.objects.all()
    }
