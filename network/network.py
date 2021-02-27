from pygan.ebgan_image_generator import EBGANImageGenerator
from logging import getLogger, StreamHandler, NullHandler, DEBUG, ERROR
import mxnet as mx
from PIL import Image, ImageDraw

logger = getLogger("accelbrainbase")
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

def train_network():
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
        batch_size=40,
        # `float` of learning rate.
        learning_rate=1e-06,
        # context for the network to run in
        ctx = mx.cpu()
    )

    try:
        ebgan_image_generator.EBGAN.generative_model.load_parameters("networks/edmgan.network")
        pass
    except Exception as e:
        print("no model found")

    ebgan_image_generator.learn(
        # `int` of the number of training iterations.
        iter_n=1,
        # `int` of the number of learning of the discriminative model.
        k_step=10,
    )

    ebgan_image_generator.EBGAN.generative_model.save_parameters("networks/edmgan.network")

    arr = ebgan_image_generator.EBGAN.generative_model.draw().asnumpy()
    image = arr[0, 0]
    img = Image.new(size = (128, 96), mode = "RGB")
    img_drawer = ImageDraw.Draw(img)
    print(arr)
    for y in range(len(image)):
        for x in range(len(image[y])):
            print(image[y, x])
            g = int(255 * (1 if image[y][x] > 0.5 else 0))
            img_drawer.point((x,y), fill = (g,g,g))
    img.show()
    print("Training model")

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
        learning_rate=1e-06,
        # context for the network to run in
        ctx = mx.cpu()
    )
    try:
        ebgan_image_generator.EBGAN.generative_model.load_parameters("networks/edmgan.network")
        pass
    except Exception as e:
        print("no model found")
    print("Generating output")
    return arr = ebgan_image_generator.EBGAN.generative_model.draw().asnumpy()[0, 0]
