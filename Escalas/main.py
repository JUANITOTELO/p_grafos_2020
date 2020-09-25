import music21 as m
import os
aDir=os.getcwd()
nombre = 'Escala Cromática'
song = m.converter.parse('{0}/ArchiXml/{1}.xml'.format(aDir,nombre))
#sp = m.midi.realtime.StreamPlayer(song)
#sp.play()
# process the ties
song = song.stripTies()

# unfold repetitions
i = 0
for a in song:
    if a.isStream:
        e = m.repeat.Expander(a)
        s2 = e.process()
        timing = s2.secondsMap
        song[i] = s2
    i += 1

# todo: add note onsets

def getMusicProperties(x):
    s = ''
    t=''
    r=''
    s = str(x.pitch)
    
    if x.tie != None:
        t = 't'
    elif(x.isRest):
        r = x.duration+'r'
    s += t+r
    return s


notas = []
for a in song.recurse().notes:

    if (a.isNote):
        x = a
        s = getMusicProperties(x)
        notas.append(s)

    if (a.isChord):
        n = ''
        for x in a._notes:
            s = getMusicProperties(x)
            n += ' '+s
        notas.append(n[1:])

    if (a.isRest):
        print("hola")
        x = a
        s = getMusicProperties(x)
        notas.append(s)


print("Done.")
