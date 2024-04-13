from conversion.afnd_to_afd import read_afn, afn_to_afd, generate_graphviz, recognize_word
import itertools


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

if __name__ == "__main__":
    main()
