1. finde tonhoehen mit gewicht:
    5. diese einzelnen eintraege im dict koennten dann so entstehen, indem die einzelnen gruppen eines cycles durch iteriert werden, der absolute start wert dieser gruppe berechnet wird, und dann ein allgemeiner envelope erzeugt wird der die Punkte: (abs_start_wert, 0), (abs_start_wert + attack, 1), (abs_start_wert + sustain + attack, 1), (...+release, 0) hat, und dann alle tonhoehen hinzugefuegt werden mit diesem envelope

2. finde potenzielle startpunkte fuer eine phrase (und rhythmen)
    1. praemisse: fuer jede gruppe sollte in etwa gleichen abstaenden regelmaessig punkte geben, in denen potenziell eine phrase anfangen koennte
    2. vielleicht koennten diese punkte zugleich auch das (potenziell kleinste) rhythmische grid der einzelnen phrases bestimmen
    3. moeglicherweise kannst du als rhythmisches grid immer die pulsschlaege des tiefsten partialtones einer gruppe denken
    4. fuer den fall, dass es gerade einen uebergang zwischen zwei gruppen gibt, muesste man einen interpolation zwischen beiden grids denken
        1. vielleicht eine art fiboancci transition, wo erst vor allem nur schlaege aus der gruppe die sich gerade im release befindet gewaehlt werden, und dann, je weiter der prozess fortschreitet, immer mehr eher schlaege aus der folgenden gruppe gewaehlt werden
        2. dafuer muessen alle absolute schlaege beider grids gesammelt werden und in eine liste sortiert werden (wobei die eintraege immer tuples sind (ABSOLUTE_ZEIT, GRUPPE_A_ODER_B)
        3. dann wird die fib transition durchgegangen (oder einfach gesetzte wahrscheinlichkeit, die sich aendert, zuerst hat release gewicht = 1 und attack gewicht = 0 und am ende umgekehrt), und der tuple mit den absoluten schlaegen wird durchgegangen, und wenn der naechste erwartete schlag zu gruppe 0 gehoert werden solange die absoluten zeitwerte durchgegangen bis wieder ein wert von der einen gruppe gefunden wurde usw.
        4. allerdings waere in prozess 3 vielleicht nicht verkehrt, wenn der naehcste schlag zu nahe ist (weniger als 0.5 sekunden oder so), dann wird der uebernaechste wert der entsprechende gruppe genommen
    5. jeder beat in dem rhythmus waere dann ein potenzieller startpunkt ... vielleicht ist die frage daher eher, wie man das rhythmische grid fuer eine gruppe jeweils berechnet
