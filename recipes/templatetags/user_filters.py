from django import template

from recipes.models import FollowRecipe, FollowUser, ShoppingList

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name="get_filter_values")
def get_filter_values(title):
    return title.getlist("filters")


@register.filter(name="get_filter_link")
def get_filter_link(request, tag):
    new_request = request.GET.copy()
    if tag.title in request.GET.getlist("filters"):
        filters = new_request.getlist("filters")
        filters.remove(tag.title)
        new_request.setlist("filters", filters)
    else:
        new_request.appendlist("filters", tag.title)

    return new_request.urlencode()


@register.filter(name="favorite")
def favorite(recipe, user):
    return FollowRecipe.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name="follow")
def follow(author, user):
    return FollowUser.objects.filter(user=user, author=author).exists()


@register.filter(name="shop")
def shop(recipe, user):
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()
