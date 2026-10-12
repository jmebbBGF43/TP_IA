from logic import *

prop0=Or(And(Symbol("P1"),Symbol("P2")),Symbol("B1"))
print(prop0.formula())
# ((P1) ∧ (P2)) ∨  (B1)
print(convert_to_CNF(prop0).formula())
# ((P2) ∨  (B1)) ∧ ((B1) ∨  (P1))

prop1=Biconditional(Symbol("B1"),Or(Symbol("P1"),Symbol("P2")))
print(prop1.formula())
# (B1) <=> ((P1) ∨  (P2))
print(convert_to_CNF(prop1).formula())
# ((¬(P2)) ∨  (B1)) ∧ ((B1) ∨  (¬(P1))) ∧ ((¬(B1)) ∨  (P2) ∨  (P1))

prop2=Or(Not(Symbol("C")),Empty(),And(Symbol('B'),Not(Symbol('C')),Symbol('A')))
print(prop2.formula())
# (¬C) ∨  False ∨  (B ∧ (¬C) ∧ A)
print(convert_to_CNF(prop2).formula())
# (B ∨  (¬C) ∨  False) ∧ (A ∨  (¬C) ∨  False) ∧ ((¬C) ∨  False)

prop3=And(And(Or(Symbol('A')),Or(And(Symbol("C"),Or(Symbol("E"),And(Symbol("Z"),And(Symbol("G"),Or(Symbol("H"),Or(Symbol("T"),Symbol("F")))))),Symbol('B')),And(Symbol('D'),Symbol('A'))),Symbol('C')),Or(Or(Symbol('A'),Symbol('B')),Symbol('D')))
print(prop3.formula())
# (A ∧ ((C ∧ (E ∨  (Z ∧ (G ∧ (H ∨  (T ∨  F))))) ∧ B) ∨  (D ∧ A)) ∧ C) ∧ ((A ∨  B) ∨  D)
print(flatten(prop3).formula())
# C ∧ A ∧ (B ∨  A ∨  D) ∧ ((C ∧ B ∧ (E ∨  ((F ∨  T ∨  H) ∧ G ∧ Z))) ∨  (A ∧ D))
print(convert_to_CNF(prop3).formula())
# (B ∨  D) ∧ (E ∨  D ∨  Z) ∧ (B ∨  A) ∧ (E ∨  T ∨  F ∨  A ∨  H) ∧ (E ∨  D ∨  G) ∧ (E ∨  A ∨  Z) ∧ (C ∨  D) ∧ (C ∨  A) ∧ C ∧ A ∧ (E ∨  A ∨  G) ∧ (B ∨  A ∨  D) ∧ (E ∨  T ∨  D ∨  F ∨  H)


print(And(And(prop1,Not(Symbol("B1"))),Not(Not(Symbol("P1")))).formula())
# (((B1) <=> ((P1) ∨  (P2))) ∧ (¬(B1))) ∧ (¬(¬(P1)))
print(convert_to_CNF(And(And(prop1,Not(Symbol("B1"))),Not(Not(Symbol("P1"))))).formula())
# ((B1) ∨  (¬(P1))) ∧ (P1) ∧ ((¬(B1)) ∨  (P2) ∨  (P1)) ∧ (¬(B1)) ∧ ((¬(P2)) ∨  (B1))
print(resolution_inference(And(prop1,Not(Symbol("B1"))),Not(Symbol("P1"))))
# True


