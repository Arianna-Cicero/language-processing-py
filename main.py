from conversion.afnd_to_afd import read_afn, afn_to_afd, generate_graphviz, recognize_word
from conversion.processing_exp import evaluate
import json


def main():
    afn_definition = read_afn("afnd.json")
    afd_definition = afn_to_afd(afn_definition)
    
    word = "abab"

    recognize_word(afd_definition, word)

    if afd_definition is None:
        print("Erro: nao foi possivel converter AFND para AFD.")
        return 

    afn_graph = generate_graphviz(afn_definition)
    if afn_graph is not None:
        afn_graph.render('afnd_grafo', view=True)

    afd_graph = generate_graphviz(afd_definition)
    if afd_graph is not None:
        afd_graph.render('afd_grafo', view=True)

    
    # parte b
    with open("exemplo01.er.json","r") as f:
        arvore = json.load(f)
        res,  = evaluate(arvore)
        print(res)

    with open("exemplo02.er.json","r") as f:
        arvore = json.load(f) 
        res,  = evaluate(arvore)
        print(res)

    with open("exemplo03.er.json","r") as f:
        arvore = json.load(f)
        res,  = evaluate(arvore)
        print(res)


if __name__ == "__main__":
    main()
