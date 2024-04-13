<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" width="200">
</p>

# Regular Language Recognizers

This project focuses on the implementation of regular language recognizers in the area of Language Processing. It is developed as part of a college project.

## Goals

- Demonstrate the significance of regular expressions.
- Define regular expressions for recognizing simple elements.
- Implement regular expression parsers based on deterministic finite automata (DFAs).
- Understand the process of developing tools for recognizing regular expressions.
- Implement finite automata, adapting the representation depending on determinism.
- Understand the process of converting a non-deterministic automaton into a deterministic one and specify functions for this implementation.

## Part A - Deterministic Finite Automata (AFDs)

Implementation of the AFD-based language recognition algorithm. This includes:
- Reading automaton definitions from JSON files.
- Validating the structure of the automaton.
- Generating graphical representations using the Graphviz library.
- Recognizing words.
Usage examples are provided to understand program execution and result interpretation.

## Part B - Regular Expression for Non-Deterministic Finite Automaton (AFND)

Conversion of regular expressions to AFNDs. Regular expressions are represented in JSON format. The program reads this representation and generates an equivalent AFND.

## Part C - Conversion from AFND to AFD

Development of a program that converts AFNDs into AFDs, utilizing JSON representations.
