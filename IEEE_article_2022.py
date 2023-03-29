from DPE_functions import *

# tento skript bude použitý na vytvorenie výstupov do IEEE článku
# v dátach treba iba korektne odfiltrovať X a Gamma zložku
# a validovať ju na vykreslených maticiach - All, Passed, Failed
# Toto je teda základná premisa, ale je možné prezentovať napr. aj LET
# parameter alebo iné častice, ale na to by bol potrebný správny Clusterer
# Problém - Clusterer pre DPE v1.0.5 počíta nesprávne LET
# Problém - najnovší Clusterer prijíma iba .t3pa súbory pričom z Krakowa
# sú len clog súbory