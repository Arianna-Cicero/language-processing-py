from graphviz import Digraph

def alt(args):
    return f'{args[0]}|{args[1]}'

def seq(args):
    return f'{args[0]}|{args[1]}'

def kle(args):
    return f'{args[0]}*'

def trans(args):
    return f'{args[0]}+'

operators: dict = {
    "alt": (alt, 0),
    "seq": (seq, 1),
    "kle": (kle, 2),
    "trans": (trans, 2)

}

def evaluate(arv):
    if isinstance(arv, dict):
        if 'op' in arv: 
            op, op_priority = operators[arv['op']]
            args_res = [evaluate(a) for a in arv['args']]
            processed_args = [a[0] if op_priority < a[1] else f'({a[0]})' for a in args_res]
            return op(processed_args), op_priority

        elif 'simb' in arv:
            return arv['simb'], 3

        elif 'epsilon' in arv:
            return 'ε', 3

    raise Exception("Formato de árvore de expressão regular inválido")