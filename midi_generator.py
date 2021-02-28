from midi_data_extractor import PlayedNote
from music21 import *

def convert_data_to_midi(input_data, name, percent):
    print("Turning data into midi stream")
    _stream = stream.Stream()

    invert = 1
    if percent < .50:
        invert = -1

    for x in range(len(input_data[0])) :
        notes = []
        for y in range(len(input_data)):
            if input_data[y][x] * invert > percent * invert:
                notes.append(note.Note(96 - y))
        midi_note = None
        if len(notes) > 0:
            midi_note = chord.Chord(notes)
        else:
            midi_note = note.Note(0)
        midi_note.duration.quarterLength = 0.25
        _stream.append(midi_note)
    print(f"Creating midi file with name {name}")
    _converter = converter.Converter().getSubConverterFormats()["midi"]().write(_stream, "midi", f"{name}.mid")
    return stream
