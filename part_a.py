import json
from graphviz import Source

def read_afd(file_path):
    try:
        print('Entrei no Read AFD')
        with open(file_path, "r") as f:
            afd_definition = json.load(f)
        return afd_definition
    except FileNotFoundError:
        print(f"Erro: doc '{file_path}' nao encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: doc '{file_path}' nao e um json valido.")
        return None

def generate_graph_pdf(afd_definition, output_file):
    try:
        dot_code = 'digraph {\n'
        for state in afd_definition['Q']:
            shape = 'doublecircle' if state in afd_definition['F'] else 'circle'
            dot_code += f'    {state} [shape={shape}];\n'

        for from_state, transitions in afd_definition['delta'].items():
            for symbol, to_states in transitions.items():
                for to_state in to_states:
                    dot_code += f'    {from_state} -> {to_state} [label="{symbol}"];\n'
        dot_code += '}'

        graph = Source(dot_code)
        graph.render(output_file, format='pdf', cleanup=True)
        print(f"O grafo do AFD foi guardado em '{output_file}.pdf'.")
        return True
    except KeyError as e:
        print(f"Erro: a definição de AFD falta lhe uma chave '{e}'.")
        return False

def recognize_word(afd_definition, word):
    try:
        current_state = afd_definition['q0']
        path = [current_state] 
        for symbol in word:
            if symbol not in afd_definition['V']:
                print(f"Erro: O símbolo '{symbol}' não está no alfabeto.")
                return False
            if current_state not in afd_definition['Q']:
                print(f"Erro: Estado inválido '{current_state}' encontrado.")
                return False
            if symbol in afd_definition['delta'][current_state]:
                next_state = afd_definition['delta'][current_state][symbol]
                path.append(next_state)  
                current_state = next_state
            else:
                print(f"Erro: Não há transição para o símbolo '{symbol}' do estado '{current_state}'.")
                return False
        if current_state in afd_definition['F']:
            print(f"A palavra '{word}' é reconhecida pelo AFD!")
            print(f"Caminho percorrido: {' -> '.join(path)}")
            return True
        else:
            print(f"A palavra '{word}' NÃO é reconhecida pelo AFD.")
            print(f"Caminho percorrido até a rejeição: {' -> '.join(path)}")
            return False
    except KeyError as e:
        print(f"Erro: A definição de AFD está faltando uma chave '{e}'")
        return False
    
def read_word_from_user():
    return input("Escreva a palavra a ser reconhecida pelo AFD: ")

def main():

    afd_file = "afd.json"
    afd_definition = read_afd(afd_file)
    if afd_definition:
        generate_graph_pdf(afd_definition, "afd_grafico_part_a")
        word = read_word_from_user()
        recognize_word(afd_definition, word)


if __name__ == "__main__":
    main()