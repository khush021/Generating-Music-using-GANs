from pygan.ebgan_image_generator import EBGANImageGenerator
from logging import getLogger, StreamHandler, NullHandler, DEBUG, ERROR
import mxnet as mx
from PIL import Image, ImageDraw
from midi_generator import convert_data_to_midi
import sys

logger = getLogger("accelbrainbase")
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

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

    print("Training model")
    ebgan_image_generator.learn(
        # `int` of the number of training iterations.
        iter_n=epochs,
        # `int` of the number of learning of the discriminative model.
        k_step=10,
    )

    print("Saving model to file")
    ebgan_image_generator.EBGAN.generative_model.save_parameters("networks/edmgan.network")

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
        ebgan_image_generator.EBGAN.generative_model.load_parameters("networks/edmgan.network")
        pass
    except Exception as e:
        print("No model found")
        return
    print("Generating output")
    arr = ebgan_image_generator.EBGAN.generative_model.draw().asnumpy()
    image = arr[0, 0]
    img = Image.new(size = (128, 96), mode = "RGB")
    img_drawer = ImageDraw.Draw(img)
    for y in range(len(image)):
        for x in range(len(image[y])):
            g = 255
            if image[y][x] < 0.5:
                g = 0
            img_drawer.point((x,y), fill = (g,g,g))

    print("Showing Image")
    img.show()

    name = "test"
    if len(sys.argv) > 2:
        name = sys.argv[2]

    print("Saving to midi file")
    midi = convert_data_to_midi(image, name)
    # return {image, midi, img}
