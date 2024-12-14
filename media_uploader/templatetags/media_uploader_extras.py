from django import template
register = template.Library()

@register.filter
def resolve_label(labels, index):
    label = 'unlabeled' if index == -1 else labels[index]
    return label