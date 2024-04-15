from conversion.afnd_to_afd import read_afn, afn_to_afd, generate_graphviz, recognize_word
import itertools
import sys
import json
from regex_to_afnd import parse_expression, convert_to_afnd


def main():
    # Load AFN and AFD definitions from JSON files
    afn_definition = read_afn("afnd.json")
    afd_definition = afn_to_afd(afn_definition)

    # Check if AFN to AFD conversion was successful
    if afd_definition is None:
        print("Error: Unable to convert AFN to AFD.")
        return 

    # Generate Graphviz representation of the AFN
    afn_graph = generate_graphviz(afn_definition)
    if afn_graph is not None:
        afn_graph.render('afn_graph', view=True)

    # Generate Graphviz representation of the AFD
    afd_graph = generate_graphviz(afd_definition)
    if afd_graph is not None:
        afd_graph.render('afd_graph', view=True)

    # Example word to recognize
    word = "abab"

    # Recognize the word using the AFD
    recognize_word(afd_definition, word)

     # Verifica se o número de argumentos fornecidos está correto
    if len(sys.argv) != 3:
        print("Uso: python main.py <entrada.json> <saida.json>")
        return

    input_file = sys.argv[1]  # Arquivo de entrada contendo a expressão regular em formato JSON
    output_file = sys.argv[2]  # Arquivo de saída onde o AFND resultante será salvo em formato JSON

    # Lê os dados da expressão regular do arquivo de entrada
    with open(input_file, "r") as f:
        expression_data = json.load(f)

    # Converte a expressão regular em uma árvore de expressão
    expression_tree = parse_expression(expression_data)
    if expression_tree is None:
        print("Erro ao analisar a expressão regular")
        return

    # Converte a árvore de expressão em um AFND
    afnd = convert_to_afnd(expression_tree)

    # Salva o AFND resultante no arquivo de saída
    with open(output_file, "w") as f:
        json.dump(afnd, f, indent=4)

if __name__ == "__main__":
    main()
