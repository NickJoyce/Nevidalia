from django import template
from promocode.models import Promocode

register = template.Library()

@register.simple_tag(name="distinct_parks")
def get_distinct_parks():
    return [promocode.park for promocode in Promocode.objects.distinct('park')]

@register.simple_tag(name="distinct_external_id")
def get_distinct_external_id():
    return [promocode.tilda_external_product_id  for promocode in Promocode.objects.distinct('tilda_external_product_id')]