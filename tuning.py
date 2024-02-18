import mido

'''
FORMAT OF MIDI TUNING CHANGE SYS MESSAGE
-----------------

F0 7F id 08 02 tt ll [kk xx yy zz]x(ll) F7
where

F0 7F = universal realtime SysEx header
id    = target device ID
08    = sub-id #1 (MIDI tuning standard)
02    = sub-id #2 (note change)
tt    = tuning program number from 0 to 127
ll    = number of notes to be changed (sets of [kk xx yy zz])
[kk xx yy zz] = MIDI note number, followed by frequency data for note
F7    = end of SysEx message


xx = semitone (MIDI note number to retune to, unit is 100 cents)
yy = MSB of fractional part (1/128 semitone = 100/128 cents = .78125 cent units)
zz = LSB of fractional part (1/16384 semitone = 100/16384 cents = .0061 cent units)

7F 7F 7F is reserved for no change to the existing note tuning
'''

comma1, comma2 = 100/128, 100/16384

TUNETABLE = {
   4 : -14,
   -4: +14,
   5 : -2,
   -5: +2
}

def msg_type(msg):
    if msg.type == 'note_off':
        return 'off'
    elif msg.type == 'note_on':
        return 'off' if msg.velocity == 0 else 'on'
    else:
        return msg.type

def _get_all(_cls, semshift):
   validrange = lambda n: n<128 and n>=0
   ls1 = [_cls + n*12 for n in range(11)]
   return [(n, n+semshift) for n in ls1 if
            validrange(n) and validrange(n+semshift)]

def _get_payload(note, newdeviate):
   '''
   tunes the pitch class in all octaves
   '''
   val = note*100 + newdeviate
   xx, rem = int(val//100), val%100
   yy, rem2 = int(rem//comma1), rem%comma1
   zz = int(rem2//comma2)
   tuples = _get_all(note%12, xx - note)
   appendix = () 
   for a in [t+(yy,zz) for t in tuples]:
      appendix += a
   return (127, 127, 8, 2, 0, len(tuples)) + appendix

def tuning():
   outport = mido.open_output('Midi Through Port-0')
   inport = mido.open_input('KeyRig 49 MIDI 1')
   deviations = [0 for i in range(12)] # from 12-tet 
   for msg in inport:
      if msg_type(msg) == 'on':
         for x, centdif in TUNETABLE.items():
            newdeviate = deviations[msg.note%12] + centdif
            deviations[(msg.note + x)%12] = newdeviate
            # send tuning message
            payload = _get_payload(msg.note + x, newdeviate)
            outport.send( mido.Message('sysex', data=payload) )