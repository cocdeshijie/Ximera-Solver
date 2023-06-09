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

    text = text.replace('\\answer ', '\\answer')

    while index < len(text):
        if text[index:index + 7] == '\\answer':
            index += 7
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
  F(x,y) = F(x,mx) &= \frac{2x^2\left(\answer{mx}\right)}{3x^4+4\left(\answer{mx}\right)^2} \\
  &= \frac{\answer{2m} \cdot x^3 }{3x^4 + \answer{4m^2}\cdot x^2} \\
  &= \frac{2mx}{3x^2+4m^2}
 """
def modify_latex(latex_str):
    # Define the regex pattern
    import regex
    pattern = r'(?<!\\[a-zA-Z]+)\{([^\{\}]+)\}'
    # Replace the matched pattern with the desired format
    return regex.sub(pattern, r'{(\1)}', latex_str)




matches = extract_answer_brackets(input_string)
print(matches)

modified = modify_latex(matches[0])
print(modify_latex(matches[0]))

from pylatexenc.latex2text import LatexNodes2Text


for match in matches:
    answer = (LatexNodes2Text().latex_to_text(latex=modified))
    print(answer)

