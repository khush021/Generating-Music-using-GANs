from pygan.ebgan_image_generator import EBGANImageGenerator
from logging import getLogger, StreamHandler, NullHandler, DEBUG, ERROR
import mxnet as mx
from PIL import Image, ImageDraw
from midi_generator import convert_data_to_midi
import sys
import os

# logger = getLogger("accelbrainbase")
# handler = StreamHandler()
# handler.setLevel(DEBUG)
# logger.setLevel(DEBUG)
# logger.addHandler(handler)

def train_network():
    print("Creating model")
    ebgan_image_generator = EBGANImageGenerator(
        # `list` of path to your directories.
        dir_list=[
            "edm_images",
        ],
        # `int` of image width.
        width=128,
        # `int` of image height.
        height=96,
        # `int` of image channel.
        channel=1,
        # `int` of batch size.
        batch_size=200,
        # `float` of learning rate.
        learning_rate=1e-06,
        # context for the network to run in
        ctx = mx.cpu()
    )

    print("Loading model from file")
    try:
        ebgan_image_generator.EBGAN.generative_model.load_parameters("networks/edmgan.network")
        pass
    except Exception as e:
        print("No model found.")

    epochs = 1
    if len(sys.argv) > 2:
        epochs = int(sys.argv[2])
    i = 0
    while True:
        print(f"Training model: {i}")
        ebgan_image_generator.learn(
            # `int` of the number of training iterations.
            iter_n=epochs,
            # `int` of the number of learning of the discriminative model.
            k_step=10,
        )

        print("Saving model to file")
        ebgan_image_generator.EBGAN.generative_model.save_parameters(f"networks/edmgan{i * epochs + 21}.network")
        if i % 5 == 0:
            create_midi(ebgan_image_generator, f"trains_{i * epochs + 21}_output")
        i+=1

def generate_output():
    ebgan_image_generator = EBGANImageGenerator(
        # `list` of path to your directories.
        dir_list=[
            "edm_images",
        ],
        # `int` of image width.
        width=128,
        # `int` of image height.
        height=96,
        # `int` of image channel.
        channel=1,
        # `int` of batch size.
        batch_size=1,
        # `float` of learning rate.
        learning_rate=0,
        # context for the network to run in
        ctx = mx.cpu()
    )
    try:
        ebgan_image_generator.EBGAN.generative_model.load_parameters("networks/edmgan101.network")
        pass
    except Exception as e:
        print("No model found")
        return
    name = "test"
    if len(sys.argv) > 2:
        name = sys.argv[2]
    create_midi(ebgan_image_generator, name)

def create_midi(ebgan_image_generator, name):
    print("Generating output")
    arr = ebgan_image_generator.EBGAN.generative_model.draw().asnumpy()
    image = arr[0, 0]
    img_max = 0
    img_min = 1
    for y in range(len(image)):
        for x in range(len(image[y])):
            img_max = max(img_max, image[y][x])
            img_min = min(img_min, image[y][x])

    for y in range(len(image)):
        for x in range(len(image[y])):
            image[y,x] -= img_min
            image[y,x] /= (img_max - img_min)

    os.mkdir(f"{name}")

    for i in range(1, 20):
        img = Image.new(size = (128, 96), mode = "RGB")
        img_drawer = ImageDraw.Draw(img)
        invert = 1
        if i <= 10:
            invert = -1

        for y in range(len(image)):
            for x in range(len(image[y])):
                g = 255
                if image[y][x] * invert < invert * i / 20:
                    g = 0
                img_drawer.point((x,y), fill = (g,g,g))
        img.show()
        os.mkdir(f'{name}/{i * 5}_percent')
        img.save(f'{name}/{i * 5}_percent/image.png')
        print("Saving to midi file")
        midi = convert_data_to_midi(image, f"{name}/{i * 5}_percent/midi" , i / 20)
    # return {image, midi, img}
