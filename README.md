# taxes

This module computes federal taxes and state taxes for a given gross salary. 
# Usage 
```
from taxes import Taxer
t = Taxer('Calif.', 'Joint')
salary = 30000
federal_tax = t.federal_tax(salary)
state_tax = t.state_tax(salary)
net_income = t.net_income(salary)
```

# Data 
## `status` Values
- `Single` - filing as not married 
- `Joint` - filing as married

## `state` Values 
```
Ala.
Alaska
Ariz.
Ark.
Calif.
Colo.
Conn.
D.C.
Del.
Fla.
Ga.
Hawaii
Idaho
Ill.
Ind.
Iowa
Kans.
Ky.
La.
Maine
Mass.
Md.
Mich.
Minn.
Miss.
Mo.
Mont.
N.C.
N.D.
N.H.
N.J.
N.M.
N.Y.
Nebr.
Nev.
Ohio
Okla.
Ore.
Pa.
R.I.
S.C.
S.D.
Tenn.
Tex.
Utah
Va.
Vt.
W.Va.
Wash.
Wis.
Wyo.
```
