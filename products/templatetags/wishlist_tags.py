from django import template

register = template.Library()

@register.filter
def is_in_wishlist(product_id, wishlist_items):
    if not wishlist_items:
        return False
    # Use an in-memory cache set to avoid N+1 query problems in loops
    if not hasattr(wishlist_items, '_product_ids_cache'):
        try:
            wishlist_items._product_ids_cache = set(wishlist_items.values_list('product_id', flat=True))
        except Exception:
            wishlist_items._product_ids_cache = set(item.product_id for item in wishlist_items)
    return product_id in wishlist_items._product_ids_cache
