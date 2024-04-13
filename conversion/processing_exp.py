import json

# Definição das funções para cada operação
def alt(args):  # args = ['a','ab'] -> args = ["a"]
    return f'{args[0]}|{args[1]}'

def seq(args):
    return f'{args[0]}{args[1]}'

def kle(args):
    return f'{args[0]}*'

def trans(args):
    return f'{args[0]}+'


# Dicionário de operadores para mapear operações e suas prioridades
operadores = {
    "alt": (alt, 0),     # união            |
    "seq": (seq, 1),     # concatenação     .
    "kle": (kle, 2),     # fecho de kleene  *
    "trans": (trans, 2)  # fecho transitivo +
}

def evaluate(arv):
    # Avalia operadores, símbolos e epsilon
    if isinstance(arv, dict):
        if 'op' in arv:  # Avalia operações
            op, op_priority = operadores[arv['op']]
            args_res = [evaluate(a) for a in arv['args']]
            # Processa os argumentos com base na prioridade
            processed_args = [a[0] if op_priority < a[1] else f'({a[0]})' for a in args_res]
            return op(processed_args), op_priority

        elif 'simb' in arv:
            return arv['simb'], 3

        elif 'epsilon' in arv:
            return 'ε', 3

    raise Exception("Formato de árvore de expressão regular inválido")

def main():
    with open("expressoes_regulares.json", "r") as f:
        expressoes_regulares = json.load(f)

    for nome, arvore in expressoes_regulares.items():
        try:
            resultado, _ = evaluate(arvore)
            print(f"A expressão regular '{nome}' é: {resultado}")
        except Exception as e:
            print(f"Erro ao avaliar a expressão regular '{nome}': {e}")

if __name__ == "__main__":
    main()
