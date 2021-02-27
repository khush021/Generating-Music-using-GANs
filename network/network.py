from pygan.ebgan_image_generator import EBGANImageGenerator
from logging import getLogger, StreamHandler, NullHandler, DEBUG, ERROR
import mxnet as mx

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

    # ebgan_image_generator.learn(
    #     # `int` of the number of training iterations.
    #     iter_n=0,
    #     # `int` of the number of learning of the discriminative model.
    #     k_step=10,
    # )

    # ebgan_image_generator.EBGAN.generative_model.save_parameters("/networks/edmgan.network")

    # arr = ebgan_image_generator.EBGAN.generative_model.draw()
    print("Training model")

def generate_output():
    print("Generating output")
