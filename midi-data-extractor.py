"""
The midi-data-extractor.py computes pitches and durations of notes for given midi files and maps
them to their corresponding midi file names in a dictionary.

ATTRIBUTES
---------
all_pitches
    a dictionary of midi file names and their corresponding note pitches
all_durations
    a dictionary of midi file names and their corresponding note durations

COMMON USE CASES FOR 'Pitch' OBJECT:
---------
Pitch.midi
    Midi value of pitch. Example: 67.
Pitch.fullName
    Full name of pitch. Example: 'G in octave 4'.
Pitch.name
    Name of pitch. Example: 'G'.
Pitch.octave
    Octave pitch is in. Example: '4'.

COMMON USE CASES FOR 'Duration' OBJECT:
---------
Duration.fullName
    Full name of note duration. Example: 'Eighth Triplet (1/3 QL)'.
Duration.quarterLength
    Duration of note where quarter note is 1.0. Example: '0.5'.
"""


from music21 import converter, note, chord, instrument
import glob


# Maps pitches and note durations to their corresponding input midi file
all_pitches = {}
all_durations = {}

for file in glob.iglob(r'edm_midi/*.mid'):
    notes = []
    duration = []
    midi = converter.parse(file)
    notes_to_parse = None
    instrument_parts = instrument.partitionByInstrument(midi)
    if instrument_parts:  # File is partitioned by instrument
        notes_to_parse = instrument_parts.parts[0].recurse()
    else:
        notes_to_parse = midi.flat.notes
    for elem in notes_to_parse:
        if isinstance(elem, note.Note):
            notes.append(elem.pitch)
            duration.append(elem.duration)
        elif isinstance(elem, chord.Chord):
            notes.append('.'.join(str(n) for n in elem.normalOrder))
    if len(notes) != 0:  # Filter out songs with no notes and chords
        all_pitches[str(file)] = notes
        all_durations[str(file)] = duration
