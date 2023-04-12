import re

test1 = r"""<![CDATA[ 
 \text {When $x=0$, the cross-sections are given by } z=\answer {|y|}  
]]>
"""


pattern = r'\\answer\s*{([^{}]*(?:{(?:[^{}]*(?:{[^{}]*})*[^{}]*)*})*[^{}]*)}'
answer_matches = re.findall(pattern, test1)

import sympy as sp
from sympy.parsing.latex import parse_latex

def tex_to_unicode(tex_expression):
    expr = parse_latex(tex_expression)
    expr = sp.pretty(expr, use_unicode=False)
    return expr

answers = []
for answer in answer_matches:
    answers.append(tex_to_unicode(str(answer)))

print(answers)
print(tex_to_unicode('3/2'))


