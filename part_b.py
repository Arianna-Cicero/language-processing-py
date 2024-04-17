import json

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

    def process_node(node, current_state):
        if "simb" in node:
            symbol = node["simb"]
            afnd["V"].append(symbol)
            next_state = current_state + 1
            afnd["Q"].append(current_state)
            afnd["Q"].append(next_state)
            add_transition(current_state, symbol, next_state)
            return next_state
        elif "op" in node:
            if node["op"] == "alt":
                left_state = process_node(node["args"][0], current_state)
                right_state = process_node(node["args"][1], current_state)
                afnd["q0"] = current_state
                afnd["F"].extend([left_state, right_state])
                return right_state + 1
            elif node["op"] == "seq":
                left_state = process_node(node["args"][0], current_state)
                right_state = process_node(node["args"][1], left_state)
                afnd["q0"] = current_state
                afnd["F"].append(right_state)
                return right_state + 1
            elif node["op"] == "kle":
                kleene_state = process_node(node["args"][0], current_state)
                afnd["q0"] = current_state
                afnd["F"].append(kleene_state)
                add_transition(kleene_state, "ε", current_state)
                add_transition(kleene_state, "ε", kleene_state + 1)
                afnd["Q"].append(current_state)
                afnd["Q"].append(kleene_state + 1)
                return kleene_state + 2
        return current_state

    process_node(expression_tree, current_state)

    return afnd

def main():
    input_file = "exemplo03.er.json"
    output_file = "afnd_output.json"

    with open(input_file, "r") as f:
        expression_tree = json.load(f)

    afnd_definition = evaluate(expression_tree)

    afnd_definition = convert_to_afnd(expression_tree)

    with open(output_file, "w") as f:
        json.dump(afnd_definition, f, indent=4)


if __name__ == "__main__":
    main()