import sys
from pedal import sus_pedal
from tuning import tuning
from file_correction import file_correction

def prompt():
   return '''
usage:
      -p              sustain pedal on left mouse button
      -t              real-time tuning of fifths and thirds above and below      
      -f FILE DELAY   sustain pedal timing correction for musescore midi output
   '''

# cli
assert len(sys.argv) > 1, prompt()
if sys.argv[1] == '-p':
   sus_pedal()
elif sys.argv[1] == '-f':
   assert len(sys.argv) == 4, prompt()
   file_correction(sys.argv[2], float(sys.argv[3]))
elif sys.argv[1] == '-t':
   tuning()
else:
   prompt()