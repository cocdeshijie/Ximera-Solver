import re

def extract_answers(input_string):
    pattern = r'\\answer\s*{([^{}]*)}'
    answers = []

    for match in re.finditer(pattern, input_string):
        nested_str = match.group(1)
        nested_str = extract_answers(nested_str)
        answers.append("".join(nested_str) if nested_str else match.group(1))

    return answers



import sympy as sp
from sympy.parsing.latex import parse_latex

def tex_to_unicode(tex_expression):
    expr = parse_latex(tex_expression)
    expr = sp.pretty(expr, use_unicode=False)
    return expr



def extract_answers(input_string):
    pattern = r'\\answer\s*{((?:[^{}]|{[^{}]*})*)}'
    answers = []

    for match in re.finditer(pattern, input_string):
        answers.append(match.group(1))

    return answers


def extract_answer_brackets(text):
    result = []
    stack = []
    index = 0

    while index < len(text):
        if text[index:index + 8] == '\\answer ':
            index += 8
            if text[index] == '{':
                stack.append(index)
                level = 1
                index += 1
                start = index

                while index < len(text) and level > 0:
                    if text[index] == '{':
                        level += 1
                    elif text[index] == '}':
                        level -= 1
                    index += 1

                if level == 0:
                    result.append(text[start:index - 1])
        else:
            index += 1

    return result

input_string = r"""
\answer {\sqrt {e^{2t}+\cos ^{2}(t)}}
 """

matches = extract_answer_brackets(input_string)


from pylatexenc.latex2text import LatexNodes2Text

for match in matches:
    print(LatexNodes2Text().latex_to_text(latex=match))
