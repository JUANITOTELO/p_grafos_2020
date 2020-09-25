import xml.dom.minidom
import sys
import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
import pandas as pd
import IPython.display as ipd
import music21 as m21

# Decimos donde se encuentran las herramientas y el archivo xml
aDir=os.getcwd()
m21.environment.set('lilypondPath','/usr/bin/lilypond')
m21.environment.set('midiPath','/usr/bin/lilymidi')
m21.environment.set('graphicsPath','/usr/bin/fim')
fn = os.path.join('{0}/fur_elise.xml'.format(aDir))

# Convertimos el archivo para poderlo procesar
s = m21.converter.parse(fn)
lastOM = s.parts[0].getElementsByClass('Measure')[-1].number
# Se crea la lista para almacenar las notas para nuestro grafo
notas = []

for i in range(lastOM):
    miau1 = s.measure(i+1)
    # miau1.parts[0].show('text')
    guau1 = miau1.parts[0].pitches
    notas += [str(p) for p in guau1]

print(notas)