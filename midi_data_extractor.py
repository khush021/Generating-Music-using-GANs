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
import re

# Maps pitches and note durations to their corresponding input midi file


class PlayedNote:
    def __init__(self, note, duration):
        self.note = note
        self.duration = duration

    def __str__(self):
        return f'note: {self.note}, duration: {self.duration}'

def get_midi_data():
    midi_data = {}
    min_duration = 100
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
                notes.append(str(elem.pitch.midi))
                duration.append(elem.duration.quarterLength)
                if elem.duration.quarterLength < min_duration:
                    min_duration = elem.duration.quarterLength
            elif isinstance(elem, chord.Chord):
                notes.append('.'.join(str(n) for n in elem.normalOrder))
                duration.append(elem.duration.quarterLength)
        if len(notes) != 0:  # Filter out songs with no notes and chords
            cleaned_file_name = re.findall(r'edm_midi\\(.*)\.mid', str(file))[0]
            midi_data[cleaned_file_name] = [None] * len(notes)
            for i in range(len(notes)):
                midi_data[cleaned_file_name][i] = PlayedNote(notes[i], duration[i])
    return midi_data
