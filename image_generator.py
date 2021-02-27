from midi_data_extractor import PlayedNote, get_midi_data
from PIL import Image, ImageDraw

def generate_images():
    print("Generating images")
    print("Parsing midi data")
    midi_data = get_midi_data()
    print("Midi data gathered")
    for name, song_data in midi_data.items():
        length = 0
        for note in song_data:
            length += note.duration
        img = Image.new(mode = "RGB", size = (128, 96))
        drawer = ImageDraw.Draw(img)
        current_index = 0
        image_num = 0
        for note in song_data:
            for sub_note in note.note.split("."):
                drawer.line([(current_index, 96 - int(sub_note)), (current_index + note.duration * 4, 96 - int(sub_note))], fill = (255, 255, 255))
            # img.show()
            current_index += note.duration * 4

            if current_index % 96 != current_index:
                current_index = 0
                img.save(f'edm_images/{name.replace(" ", "_")}_{image_num}.png')
                image_num += 1
                img = Image.new(mode = "RGB", size = (128, 96))
                drawer = ImageDraw.Draw(img)
        img.save(f'edm_images/{name.replace(" ", "_")}_{image_num}.png')
