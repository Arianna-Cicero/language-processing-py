import itertools
import json
from graphviz import Digraph


def read_afnd(file_path):
    try:
        print('entrei a ler o AFND...')
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
        print(f"O gráfico do AFD foi guardado em '{output_file}.pdf'.")
        return True
    except KeyError as e:
        print(f"Erro: a definição de AFD falta-lhe uma chave '{e}'.")
        return False



def afnd_to_afd(afnd_definition):
    try:
        print("entre a converter afnd para afd")
        afnd_states = afnd_definition['Q']
        afnd_alphabet = afnd_definition['V']
        afnd_delta = afnd_definition['delta']
        afnd_initial_state = afnd_definition['q0']
        afnd_final_states = afnd_definition['F']

        afnd_states_combinations = [tuple(sorted(set(states))) for states in
                                   itertools.chain.from_iterable(
                                       itertools.combinations(afnd_states, r) for r in range(len(afnd_states) + 1))]

        afn_states_combinations_map = {combination: i for i, combination in enumerate(afnd_states_combinations)}

        afd_definition = {
            'Q': [],
            'V': afnd_alphabet,
            'q0': None,
            'F': [],
            'delta': {}
        }

        for combination in afnd_states_combinations:
            afd_state = ''.join(combination)
            afd_definition['Q'].append(afd_state)
            if afnd_initial_state in combination:
                afd_definition['q0'] = afd_state
            if any(state in combination for state in afnd_final_states):
                afd_definition['F'].append(afd_state)

        for combination in afnd_states_combinations:
            afd_state = ''.join(combination)
            afd_definition['delta'][afd_state] = {}

            for symbol in afnd_alphabet:
                destination_states = set()
                for state in combination:
                    if state in afnd_delta and symbol in afnd_delta[state]:
                        destination_states.update(afnd_delta[state][symbol])
                if destination_states:
                    destination_combination = tuple(sorted(destination_states))
                    destination_state = afn_states_combinations_map[destination_combination]
                    afd_definition['delta'][afd_state][symbol] = afd_definition['Q'][destination_state]

        print('Conversão AFND para AFD feitinha.')
        return afd_definition
    except KeyError as e:
        print(f"Erro: AFND falta lhe uma chave '{e}'")
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