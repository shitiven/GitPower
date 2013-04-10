# encoding: utf-8
'''highlight code template filter'''

from django import template
from pygments import highlight, formatters
from pygments.lexers import guess_lexer_for_filename

register = template.Library()


@register.filter
def highlight_blob(filename, code):
    '''highlight for blob data'''

    formatter = formatters.HtmlFormatter(
          linenos=True,
          encoding='utf-8',
          style = 'friendly',
          noclasses="False")

    lexer = guess_lexer_for_filename(filename, code, encoding='utf-8')
    result = highlight(code, lexer, formatter)
    return result


@register.filter
def highlight_blob_css():
    '''get highlight css style'''

    formatter = formatters.HtmlFormatter(
          linenos=True,
          encoding='utf-8',
          style = 'friendly',
          noclasses="True")

    return formatter.get_style_defs()





