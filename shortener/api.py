from ninja import Router
from .schemas import LinkSchema
from .models import Links
from django.shortcuts import get_object_or_404

shortener_router = Router()

@shortener_router.post('/', response={200: LinkSchema, 409: dict})
def create_shortener(request, link_schema: LinkSchema):
    data = link_schema.to_model_data()
    token = data['token']
    if token and Links.objects.filter(token=token):
        return 409, {'error': 'Token já existe, use outro'}
    link = Links(**data)
    link.save()
    return 200, LinkSchema.from_model(link)

@shortener_router.get('/{token}')
def redirect_link(request, token):
    link = get_object_or_404(Links, token=token, active=True)