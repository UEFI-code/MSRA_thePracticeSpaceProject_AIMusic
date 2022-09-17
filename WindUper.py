import torch
import miditoolkit

def ArrayToMidi(data, savepath):
    mido_obj = miditoolkit.midi.parser.MidiFile()
    beat_resol = mido_obj.ticks_per_beat

    # create an  instrument
    track = miditoolkit.midi.containers.Instrument(program=0, is_drum=False, name='myTrack')
    mido_obj.instruments = [track]

    # create eighth notes
    duration = int(beat_resol * 0.5)
    prev_end = 0
    pitch = 60
    for i in data:
        # create one note
        start = prev_end
        end = prev_end + duration
        for j in range(3):
            pitch = int(i[j * 2])
            velocity = int(i[j * 2 + 1])
            if pitch in range(0,128) and velocity in range(0,128):
                note = miditoolkit.midi.containers.Note(start=start, end=end, pitch=pitch, velocity=velocity)
                mido_obj.instruments[0].notes.append(note)
        # prepare next
        prev_end = end

    # create markers
    marker_hi = miditoolkit.midi.containers.Marker(time=0, text='2333')
    mido_obj.markers.append(marker_hi)

    # write to file
    mido_obj.dump(savepath)

#sample = [[66,55,77,88,99,44], [77,88,66,99,99,100], [75,98,34,79,56,90]]
#ArrayToMidi(sample, '/tmp/test.midi')
