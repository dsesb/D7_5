from django import template

register = template.Library()

CENS = ['дура', 'тупая', 'somebigtext', 'new']


@register.filter()
def censor(text):
    text_cens = ''
    for word in text.split():
        if word.strip('.,"/') in CENS:
            word = (word[:1] + ('*' * (len(word) - 1)))
        text_cens += f'{word + " "}'
    return text_cens
