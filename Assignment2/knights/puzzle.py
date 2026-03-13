###### --------------------------------------------
## The author of these scripts is T. D. Devlin 
###### --------------------------------------------

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 1
# A says "I am both a knight and a knave."
# ----------------------------------------
##   write the statement(s) in PL
##   Structure: A is exactly one of knight/knave: AKnight ⊕ AKnave
##   A says S where S = "I am both knight and knave" = AKnight ∧ AKnave
##   Knight tells truth: AKnight ⇒ S.  Knave lies: AKnave ⇒ ¬S
##   So: (AKnight ⇒ (AKnight ∧ AKnave)) ∧ (AKnave ⇒ ¬(AKnight ∧ AKnave))
stat = None
##   Fill in the knowledge base
knowledge1 = And(
    Xor(AKnight, AKnave),  # A is exactly one of knight or knave
    Implication(AKnight, And(AKnight, AKnave)),   # if A is knight, statement is true
    Implication(AKnave, Not(And(AKnight, AKnave))),  # if A is knave, statement is false
)
# ----------------------------------------

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
# ----------------------------------------
##   write the statement(s) in PL
##   Same kind: (AKnight ∧ BKnight) ∨ (AKnave ∧ BKnave) ≡ (AKnight ⇔ BKnight)
##   Different kinds: (AKnight ∧ BKnave) ∨ (AKnave ∧ BKnight) ≡ AKnight ⊕ BKnight
##   A says same: (AKnight ⇒ Biconditional(AKnight, BKnight)) ∧ (AKnave ⇒ ¬Biconditional(...))
##   B says different: (BKnight ⇒ Xor(AKnight, BKnight)) ∧ (BKnave ⇒ ¬Xor(...))
stat = None
##   Fill in the knowledge base
_same_kind = Biconditional(AKnight, BKnight)  # A and B same type
_diff_kind = Xor(AKnight, BKnight)            # A and B different types
knowledge2 = And(
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),
    Implication(AKnight, _same_kind),
    Implication(AKnave, Not(_same_kind)),
    Implication(BKnight, _diff_kind),
    Implication(BKnave, Not(_diff_kind)),
)
# ----------------------------------------

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'." and "C is a knave."
# C says "A is a knight."
# ----------------------------------------
##   write the statement(s) in PL
##   "A said 'I am a knave'" = (AKnight ⇒ AKnave) ∧ (AKnave ⇒ ¬AKnave) — always false
##   So B says (false ∧ CKnave); if B knight then false, so B must be knave.
##   C says AKnight: (CKnight ⇒ AKnight) ∧ (CKnave ⇒ ¬AKnight)
stat = None
_a_said_knave = And(
    Implication(AKnight, AKnave),
    Implication(AKnave, Not(AKnave)),
)  # true only when ¬AKnight ∧ ¬AKnave (impossible), so always false
_b_says = And(_a_said_knave, CKnave)  # B's full statement
knowledge3 = And(
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),
    Xor(CKnight, CKnave),
    Implication(BKnight, _b_says),
    Implication(BKnave, Not(_b_says)),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),
)
# ----------------------------------------


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
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
