from logic import *
import argparse

AChevalier = Symbol("A est un chevalier")
AValet = Symbol("A est un valet")

BChevalier = Symbol("B est un chevalier")
BValet = Symbol("B est un valet")

CChevalier = Symbol("C est un chevalier")
CValet = Symbol("C est un valet")

# Énigme 1
# A dit "Je suis un valet ou l'autre personne est un valet."
# B ne dit rien.
knowledge1 = And(
    # TODO

)

# Énigme 2
# A dit "Nous sommes tous les deux des valets."
# B dit "L'un d'entre nous exactement est un chevalier."
knowledge2 = And(
    # TODO

)

# Énigme 3
# A dit "B est un valet."
# B dit "L'un d'entre nous exactement est un chevalier."
# C dit "Au moins l'un d'entre nous est un chevalier."
knowledge3 = And(
    # TODO

)

# Énigme 3
# A dit parfois "Je suis un chevalier" ou "Je suis un valet.", mais on ne sait pas qui il est.
# B dit "A dit : 'Je suis un valet'."
# B dit "C est un valet."
# C dit "A est un chevalier."
knowledge4 = And(
    # TODO
    
)


def main(args):
    def check(knowledge, symbol, args):
        if args.r:
            return resolution_inference(knowledge, symbol)
        else:
            return model_check(knowledge, symbol)

    symbols = [AChevalier, AValet, BChevalier, BValet, CChevalier, CValet]
    puzzles = [
        ("Enigme 1", knowledge1),
        ("Enigme 2", knowledge2),
        ("Enigme 3", knowledge3),
        ("Enigme 4", knowledge4)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if check(knowledge, symbol, args):
                    print(f"    {symbol}")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Search a solution for clue.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c','--model-check',
                        dest='d', action='store_true',
                        help="use model checking [default]")
    group.add_argument('-r','--resolution',
                        dest="r", action="store_true",
                        help="use resolution for inference")
    parser.set_defaults(type='d')
    args = parser.parse_args()
    main(args)
