# encoding: utf-8

from django import template
from django.utils.html import conditional_escape 
import re

register = template.Library()

def split_lines_blocks(text):
    blocks = {}
    block  = 0
    text = re.sub('\n$','',text)

    for line in text.split("\n"):
        if block and not re.search("^\@\@", line):
            blocks["block"+str(block)]["lines"].append(line)

        if re.search("^\@\@", line):
            block = block + 1

            line_numbers = re.findall(r'(\d+,\d+)', line)
            a_start_line = line_numbers[0].split(",")[0]
            a_line_number = line_numbers[0].split(",")[1]

            b_start_line  = line_numbers[1].split(",")[0]
            b_line_number = line_numbers[1].split(",")[1]

            blocks["block"+str(block)] = {}
            blocks["block"+str(block)]["meta"] = line
            blocks["block"+str(block)]["lines"] = []
            blocks["block"+str(block)]["a_start_line"]  = int(a_start_line)
            blocks["block"+str(block)]["a_line_number"] = int(a_line_number)
            blocks["block"+str(block)]["b_start_line"]  = int(b_start_line)
            blocks["block"+str(block)]["b_line_number"] = int(b_line_number)

    return blocks


def opcodes(line):
    if re.search(r'^\+', line):
        return 'add'

    if re.search(r'^\-', line):
        return 'del'

    return None


def sub_space(text):
    return re.sub(r'\s', '&nbsp;', text)


def block_to_html(block):
    arr = []
    a_num = block["a_start_line"]
    b_num = block["b_start_line"]

    html = '<tr><td class="num summary">...<span></span></td><td class="num summary"><span>...</span></td><td><p class="summary pre-code">%s</p></td></tr>' % conditional_escape(block["meta"])
    arr.append(html)

    for line in block["lines"]:

        line = sub_space(conditional_escape(line))

        if opcodes(line) == 'add':
            html = '<tr><td class="num add"><span></span></td><td class="num add"><span>%s</span></td><td><p class="add pre-code">%s</p></td></tr>' % (str(b_num), line)
            arr.append(html)

            b_num = b_num + 1

        elif opcodes(line) == 'del':
            html = '<tr><td class="num del"><span>%s</span></td><td class="num del"><span></span></td><td><p class="del pre-code">%s</p></td></tr>' % (str(a_num), line)
            arr.append(html)

            a_num = a_num + 1

        else:
            html = '<tr class="nochange-hide"><td class="num"><span>%s</span></td><td class="num"><span>%s</span></td><td><p class="pre-code">%s</p></td></tr>' % (str(a_num), str(b_num), line)
            arr.append(html)

            a_num = a_num + 1
            b_num = b_num + 1

    return ''.join(arr)


@register.filter
def diff_to_html(diff):
    html  = '<table class="diff-code" cellPadding="0"><tbody>'
    
    blocks = split_lines_blocks(diff)
    for i in range(1, blocks.__len__()+1):
        html += block_to_html(blocks["block"+str(i)])

    html += '</tbody></table>'

    return html
