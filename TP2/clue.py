import argparse

from logic import *

mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")
characters = [mustard, plum, scarlet]

ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [ballroom, kitchen, library]

knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

symbols = characters + rooms + weapons




def check_knowledge(knowledge,args):
    def check(knowledge, symbol, args):
        if args.r:
            return resolution_inference(knowledge, symbol)
        else:
            return model_check(knowledge, symbol)

    for symbol in symbols:
        if check(knowledge, symbol, args):
            print(f"{symbol}: YES")
        elif not check(knowledge, Not(symbol), args):
            print(f"{symbol}: MAYBE")


# There must be a person, room, and weapon.
knowledge = And(
    Or(mustard, plum, scarlet),
    Or(ballroom, kitchen, library),
    Or(knife, revolver, wrench)
)

# Initial cards
knowledge.add(And(
    Not(mustard), Not(kitchen), Not(revolver)
))

# Unknown card
knowledge.add(Or(
    Not(scarlet), Not(library), Not(wrench)
))

# Known cards
knowledge.add(Not(plum))
knowledge.add(Not(ballroom))


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

check_knowledge(knowledge,args)
