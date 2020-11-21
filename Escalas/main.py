import Escalas as E
from alive_progress import alive_bar
import time

with alive_bar(12,spinner = 'notes2') as bar:
    for i in range(12):
        E.crear_escala("m",i)
        E.crear_escala("M",i)
        E.crear_escala("t",i)
        time.sleep(0.002)
        bar()