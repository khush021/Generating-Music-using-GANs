import sys
import image_generator as img_gen
import network.network as network

def main():
    command = ""
    if len(sys.argv) == 1:
        command = input("What part of the program do you want to run?\n1. Export midi to image files\n2. Train the network\n3. Generate an output\n")
    else:
        command = sys.argv[1]

    if command == "1":
        img_gen.generate_images()
    elif command == "2":
        network.train_network()
    else:
        network.generate_output()

if __name__ == '__main__':
    main()
