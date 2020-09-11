import ast
import math
import cmath
import operator

ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}

names = {
    'pi': cmath.pi,
    'e': cmath.e,
    'tau': cmath.tau,
    'inf': cmath.inf,
    'infj': cmath.infj,
    'nan': cmath.nan,
    'nanj': cmath.nanj,
    'max': max,
    'min': min,
    'round': round,
    'ceil': math.ceil,
    'floor': math.floor,
    'gcd': math.gcd,
    'erf': math.erf,
    'erfc': math.erfc,
    'gamma': math.gamma,
    'lgamma': math.lgamma,
    'abs': abs,
    'pow': pow,
    'phase': cmath.phase,
    'polar': cmath.polar,
    'exp': cmath.exp,
    'log': cmath.log,
    'sqrt': cmath.sqrt,
    'cos': cmath.cos,
    'acos': cmath.acos,
    'sin': cmath.sin,
    'asin': cmath.asin,
    'tan': cmath.tan,
    'atan': cmath.atan,
    'cosh': cmath.cosh,
    'acosh': cmath.acosh,
    'sinh': cmath.sinh,
    'asinh': cmath.asinh,
    'tanh': cmath.tanh,
    'atanh': cmath.atanh,
}

class Calculator:
    def __init__(self, names=dict(), ops=dict()):
        assert isinstance(names, dict)
        assert isinstance(ops, dict)
        self.names = names
        self.ops = ops

    def setOps(self, ops):
        assert isinstance(ops, dict)
        self.ops = ops

    def setNames(self, names):
        assert isinstance(names, dict)
        self.names = names

    def cal(self, expr):
        root = ast.parse(expr, mode='eval').body
        nodes = [root]
        vs = dict()
        while len(nodes) > 0:
            node = nodes.pop()
            if isinstance(node, ast.Num): # <number>
                vs[id(node)] = node.n
            elif isinstance(node, ast.BinOp): # <left> <operator> <right>
                if all([id(node.left) in vs, id(node.right) in vs]):
                    if type(node.op) in self.ops:
                        vs[id(node)] = ops[type(node.op)](vs[id(node.left)], vs[id(node.right)])
                    else:
                        name = type(node.op).__name__
                        raise SyntaxError(f'not supported binary operator \'{name}\'')
                else:
                    nodes.append(node)
                    nodes.append(node.left)
                    nodes.append(node.right)
            elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
                if id(node.operand) in vs:
                    if type(node.op) in self.ops:
                        vs[id(node)] = ops[type(node.op)](vs[id(node.operand)])
                    else:
                        name = type(node.op).__name__
                        raise SyntaxError(f'not supported unitary operator \'{name}\'')
                else:
                    nodes.append(node)
                    nodes.append(node.operand)
            elif isinstance(node, ast.Name):
                if node.id in self.names:
                    vs[id(node)] = self.names[node.id]
                else:
                    name = node.id
                    raise SyntaxError(f'not supported expression \'{name}\'')
            elif isinstance(node, ast.Call):
                vlist = [id(node.func) in vs] + [id(arg) in vs for arg in node.args]
                if all(vlist):
                    vs[id(node)] = vs[id(node.func)](*[vs[id(arg)] for arg in node.args])
                else:
                    nodes.append(node)
                    nodes.append(node.func)
                    nodes += node.args
            else:
                name = type(node).__name__
                raise SyntaxError(f'not supported expression \'{name}\'')
        return vs[id(root)]

if __name__ == '__main__':
    calculator = Calculator(names, ops)
    print(calculator.cal('+5+6*((25-9/2)-3*5/85/-12-22*5)-53/-2+(-2/(2+5-3*5*-5))'))
    print(calculator.cal('2*2**-2*(-2/-2-3+5+5+(6**2)+6**(2-3)-5*6/-2)'))
    print(calculator.cal('(2-3)**(2/3)'))
    print(calculator.cal('asin(2)'))
