import json

def parse_expression(expression):
    # Definir padrões para identificar operadores e símbolos de alfabeto
    operator_pattern = r'[\|\*\+]'
    alphabet_symbol_pattern = r'[a-zA-Z]'

    tokens = []
    i = 0

    while i < len(expression):
        char = expression[i]

        # Verificar se o caractere é um operador
        if re.match(operator_pattern, char):
            tokens.append({'type': 'OPERATOR', 'value': char})
            i += 1
        # Verificar se o caractere é um símbolo de alfabeto
        elif re.match(alphabet_symbol_pattern, char):
            tokens.append({'type': 'ALPHABET_SYMBOL', 'value': char})
            i += 1
        else:
            # Ignorar espaços em branco e outros caracteres
            if not char.isspace():
                print(f"Caractere inválido: {char}")
            i += 1

    return tokens

def convert_to_afnd(expression_tree):
    afnd = {
        "Q": [],
        "V": [],
        "q0": None,
        "F": [],
        "delta": {}
    }

    current_state = 0

    def add_transition(from_state, symbol, to_state):
        if from_state not in afnd["delta"]:
            afnd["delta"][from_state] = {}
        if symbol not in afnd["delta"][from_state]:
            afnd["delta"][from_state][symbol] = []
        afnd["delta"][from_state][symbol].append(to_state)

    def process_node(node):
        nonlocal current_state
        if "simb" in node:
            # Processar um símbolo
            symbol = node["simb"]
            afnd["V"].append(symbol)
            next_state = current_state + 1
            add_transition(current_state, symbol, next_state)
            current_state = next_state
            afnd["Q"].append(current_state)
        elif "op" in node:
            # Processar um operador
            if node["op"] == "alt":
                # Processar operador de alternância |
                pass
            elif node["op"] == "seq":
                # Processar operador de concatenação .
                pass
            elif node["op"] == "kle":
                # Processar operador de fecho de Kleene *
                pass
            # Adicionar lógica para outros operadores

    # Chamar a função de processamento do nó raiz
    process_node(expression_tree)

    # Definir o estado inicial e os estados finais
    afnd["q0"] = 0
    afnd["F"].append(current_state)

    return afnd
