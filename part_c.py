import itertools
import json
from graphviz import Digraph


def read_afnd(file_path):
    try:
        print('Entrando na leitura do AFND...')
        with open(file_path, "r") as f:
            afnd_definition = json.load(f)
        return afnd_definition
    except FileNotFoundError:
        print(f"Erro: arquivo '{file_path}' não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: arquivo '{file_path}' não é um JSON válido.")
        return None


def generate_graph_pdf(afd_definition, output_file):
    try:
        dot = Digraph(comment='Automaton')

        for state in afd_definition['Q']:
            shape = 'doublecircle' if state in afd_definition['F'] else 'circle'
            dot.node(state, shape=shape)

        for from_state, transitions in afd_definition['delta'].items():
            for symbol, to_states in transitions.items():
                for to_state in to_states:
                    dot.edge(from_state, to_state, label=symbol)

        dot.render(output_file, format='pdf', cleanup=True)
        print(f"O gráfico do AFD foi salvo em '{output_file}.pdf'.")
        return True
    except KeyError as e:
        print(f"Erro: a definição de AFD está faltando uma chave '{e}'.")
        return False



def afnd_to_afd(afn_definition):
    try:
        print('Convertendo AFND para AFD...')
        afn_states = afn_definition['Q']
        afn_alphabet = afn_definition['V']
        afn_delta = afn_definition['delta']
        afn_initial_state = afn_definition['q0']
        afn_final_states = afn_definition['F']

        # Passo 1: Gerar todas as combinações de estados do AFND
        afn_states_combinations = [tuple(sorted(set(states))) for states in
                                   itertools.chain.from_iterable(
                                       itertools.combinations(afn_states, r) for r in range(len(afn_states) + 1))]

        # Passo 2: Mapear as combinações de estados do AFND para os estados do AFD
        afn_states_combinations_map = {combination: i for i, combination in enumerate(afn_states_combinations)}

        # Passo 3: Inicializar a definição do AFD
        afd_definition = {
            'Q': [],
            'V': afn_alphabet,
            'q0': None,
            'F': [],
            'delta': {}
        }

        # Passo 4: Gerar os estados do AFD
        for combination in afn_states_combinations:
            afd_state = ''.join(combination)
            afd_definition['Q'].append(afd_state)
            if afn_initial_state in combination:
                afd_definition['q0'] = afd_state
            if any(state in combination for state in afn_final_states):
                afd_definition['F'].append(afd_state)

        # Passo 5: Gerar a função de transição do AFD
        for combination in afn_states_combinations:
            afd_state = ''.join(combination)
            afd_definition['delta'][afd_state] = {}

            for symbol in afn_alphabet:
                destination_states = set()
                for state in combination:
                    if state in afn_delta and symbol in afn_delta[state]:
                        destination_states.update(afn_delta[state][symbol])
                if destination_states:
                    destination_combination = tuple(sorted(destination_states))
                    destination_state = afn_states_combinations_map[destination_combination]
                    afd_definition['delta'][afd_state][symbol] = afd_definition['Q'][destination_state]

        print('Conversão AFND para AFD concluída.')
        return afd_definition
    except KeyError as e:
        print(f"Erro: AFND está faltando uma chave '{e}'")
        return None


def generate_afd_json(afd_definition, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(afd_definition, f, indent=4)
        print(f"O arquivo '{output_file}' foi criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o arquivo '{output_file}': {str(e)}")


def main():
    afnd_definition = read_afnd("afnd.json")
    if afnd_definition:
        generate_graph_pdf(afnd_definition, "afnd_grafico_part_c")
        afd_definition = afnd_to_afd(afnd_definition)
        if afd_definition:
            generate_afd_json(afd_definition, "afd_part_c.json")
            generate_graph_pdf(afd_definition, "afd_grafico_part_c")

if __name__ == "__main__":
    main()