from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# structure claims two sentences:
# 1. Every person is either a Knight or a Knave
# 2. No person can be both
structureA = (
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnight)),
    )

structureAB = (
    And(Or(AKnight, AKnave), Or(BKnight, BKnave)),
    Not(Or(And(AKnight, AKnave), And(BKnight, BKnave))),
    )

structureABC = (
    And(Or(AKnight, AKnave), Or(BKnight, BKnave), Or(CKnight, CKnave)),
    Not(Or(And(AKnight, AKnave), And(BKnight, BKnave), And(CKnight, CKnave))),
    )

# Puzzle 0
# A says "I am both a knight and a knave."
puzzle0ClaimA = (And(AKnight, AKnave),)
knowledge0 = And(
    # structure
    *structureA,

    #claim
    Biconditional(AKnight, *puzzle0ClaimA),
    Biconditional(AKnave, Not(*puzzle0ClaimA)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
puzzle1ClaimA = (And(AKnave, BKnave),)
knowledge1 = And(
    # structure
    *structureAB,

    # claim
    Biconditional(AKnight, *puzzle1ClaimA),
    Biconditional(AKnave, Not(*puzzle1ClaimA))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
puzzle2claimA = (Or(And(AKnight, BKnight), And(AKnave, BKnave)),)
puzzle2claimB = (Or(And(AKnight, BKnave), And(AKnave, BKnight)),)
knowledge2 = And(
    # structure
    *structureAB,

    # claim
    Biconditional(AKnight, *puzzle2claimA),
    Biconditional(AKnave, Not(*puzzle2claimA)),
    Biconditional(BKnight, *puzzle2claimB),
    Biconditional(BKnave, Not(*puzzle2claimB))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
puzzle3claimA = (Or(AKnight, AKnave),)
puzzle3claimB = (Biconditional(*puzzle3claimA, AKnave),)
puzzle3claimB = (And(*puzzle3claimB, CKnave),)
puzzle3claimC = (AKnight,)
knowledge3 = And(
    # structure
    *structureABC,

    # claim
    Biconditional(AKnight, *puzzle3claimA),
    Biconditional(AKnave, Not(*puzzle3claimA)),
    Biconditional(BKnight, *puzzle3claimB),
    Biconditional(BKnave, Not(*puzzle3claimB)),
    Biconditional(CKnight, *puzzle3claimC),
    Biconditional(CKnave, Not(*puzzle3claimC)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
