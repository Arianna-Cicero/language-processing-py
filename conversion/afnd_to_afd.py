import json
from graphviz import Digraph
import itertools


def read_afn(file_path):
    try:
        with open(file_path, "r") as f:
            afn_definition = json.load(f)
        return afn_definition
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not a valid JSON file.")
        return None

def generate_graphviz(afn_definition):
    try:
        dot = Digraph(comment='Automaton')

        # Add nodes
        for state in afn_definition['Q']:
            shape = 'doublecircle' if state in afn_definition['F'] else 'circle'
            dot.node(state, shape=shape)

        # Add transitions
        for from_state, transitions in afn_definition['delta'].items():
            for symbol, to_states in transitions.items():
                for to_state in to_states:
                    dot.edge(from_state, to_state, label=symbol)

        return dot
    except KeyError as e:
        print(f"Error: AFN definition is missing key '{e}'")
        return None

def afn_to_afd(afn_definition):
    try:
        afn_states = afn_definition['Q']
        afn_alphabet = afn_definition['V']
        afn_delta = afn_definition['delta']
        afn_initial_state = afn_definition['q0']
        afn_final_states = afn_definition['F']

        afn_states_combinations = [tuple(sorted(set(states))) for states in itertools.chain.from_iterable(itertools.combinations(afn_states, r) for r in range(len(afn_states) + 1))]
        afn_states_combinations_map = {combination: i for i, combination in enumerate(afn_states_combinations)}

        afd_definition = {
            'Q': [],
            'V': afn_alphabet,
            'q0': None,
            'F': [],
            'delta': {}
        }

        for combination in afn_states_combinations:
            afd_state = ''.join(combination)
            afd_definition['Q'].append(afd_state)
            if afn_initial_state in combination:
                afd_definition['q0'] = afd_state
            if any(state in combination for state in afn_final_states):
                afd_definition['F'].append(afd_state)

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

        return afd_definition
    except KeyError as e:
        print(f"Error: AFN definition is missing key '{e}'")
        return None


def recognize_word(afd_definition, word):
    try:
        current_state = afd_definition['q0']
        for symbol in word:
            if symbol not in afd_definition['V']:
                print(f"Error: Symbol '{symbol}' is not in the alphabet.")
                return False
            if current_state not in afd_definition['Q']:
                print(f"Error: Invalid state '{current_state}' encountered.")
                return False
            if symbol in afd_definition['delta'][current_state]:
                current_state = afd_definition['delta'][current_state][symbol]
            else:
                print(f"Error: No transition for symbol '{symbol}' from state '{current_state}'.")
                return False
        if current_state in afd_definition['F']:
            print(f"Word '{word}' is recognized by the AFD.")
            return True
        else:
            print(f"Word '{word}' is not recognized by the AFD.")
            return False
    except KeyError as e:
        print(f"Error: AFD definition is missing key '{e}'")
        return False


# def main():
#     
#     pass

# if __name__ == "__main__":
#     main()
