import mido, os
def file_correction(fpath, delay):
   '''
   Musescore's midi output gives no time between a sustain off followed by a sustain on. This causes problems in some software like Pianoteq. This function is intended solve that problem.
   - pushes sustain_on messages `delay` seconds later while pulling the next messages back in order to avoid lagging
   - creates a new midi file with single merged track
   '''
   SUSTAIN_ON_THRESH = 63
   fdir, fname = os.path.split(fpath)
   assert fname[-4:] == '.mid', 'please provide a file with .mid extension'
   fname_raw = fname[:-4]

   raw = mido.MidiFile(fpath)
   res_track = mido.MidiTrack()
   last_tempo = None
   tick_bag = 0
   for m in raw.merged_track:
      if m.type == 'set_tempo':
         last_tempo = m.tempo
      elif m.is_cc(64) and m.value > SUSTAIN_ON_THRESH:
         tick = mido.second2tick(delay, raw.ticks_per_beat, last_tempo)
         m.time += tick
         tick_bag = tick
      elif m.time:
         x = min(tick_bag, m.time)
         m.time -= x
         tick_bag -= x
      res_track.append(m)
   res = mido.MidiFile(
      ticks_per_beat=raw.ticks_per_beat,
      filename=fname_raw+'_corrected.mid',
      tracks=[res_track],
      type=0,
   )
   res.save(os.path.join(fdir, res.filename))
