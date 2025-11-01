from django.views.generic import CreateView
from .models import Position

class PositionCreateView(CreateView):
    model = Position
    fields = ['name', 'slug']
    template_name = 'company/position_form.html'
    success_url = '/'