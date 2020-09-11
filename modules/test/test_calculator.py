#from ..calculator import parse
from modules.calculator import parse

def test_case1():
    li_case = [
        '1+1', 
        '+5+6*((25-9/2)-3*5/85/-12-22*5)-53/-2+(-2/(2+5-3*5*-5))', 
    ]
    for i in li_case:
        assert parse(i) == str(float(eval((i))))
