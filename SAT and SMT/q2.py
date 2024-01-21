from z3 import *

Ame, Bri, Can, Iri = Ints("Ame Bri Can Iri")
Bfl, Dol, Hor, Tur = Ints("Bfl Dol Hor Tur")
Bow, Han, Swi, Ten = Ints("Bow Han Swi Ten")
Black, Blue, Red, White = Ints("Black Blue Red White")

s = Solver()

s.add([And(1<= x, x <= 4) for x in [Ame, Bri, Can, Iri,
                                    Bfl, Dol, Hor, Tur,
                                    Bow, Han, Swi, Ten,
                                    Black, Blue, Red, White]])
s.add (Distinct([Ame, Bri, Can, Iri]))
s.add (Distinct([Bfl, Dol, Hor, Tur]))
s.add (Distinct([Bow, Han, Swi, Ten]))
s.add (Distinct([Black, Blue, Red, White]))

s.add (Black == 2)
s.add (Han + 2 == Iri)
s.add (Hor + 2 == Red)
s.add (Ame == Tur - 1)
s.add (Bow > Ten)
s.add (Han + 2 == White)
print(s.check())
print(s.model())
