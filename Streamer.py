import argparse

import cv2
import zmq

from camera.Camera import Camera
from constants import PORT, SERVER_ADDRESS, RESOLUTION_W, RESOLUTION_H
from utils import image_to_string


class Streamer:

    def __init__(self, server_address=SERVER_ADDRESS, port=PORT, width=RESOLUTION_W, height=RESOLUTION_H):
        """
        Tries to connect to the StreamViewer with supplied server_address and creates a socket for future use.

        :param server_address: Address of the computer on which the StreamViewer is running, default is `localhost`
        :param port: Port which will be used for sending the stream
        """

        print("Connecting to ", server_address, "at", port)
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PUB)
        self.footage_socket.connect('tcp://' + server_address + ':' + port)
        self.keep_running = True
        self.width = width
        self.height = height

    def start(self):
        """
        Starts sending the stream to the Viewer.
        Creates a camera, takes a image frame converts the frame to string and sends the string across the network
        :return: None
        """
        print("Streaming Started...")
        camera = Camera(height=self.height, width=self.width)
        camera.start_capture()
        self.keep_running = True

        while self.footage_socket and self.keep_running:
            try:
                frame = camera.current_frame.read()  # grab the current frame
                image_as_string = image_to_string(frame)
                self.footage_socket.send(image_as_string)

            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break
        print("Streaming Stopped!")
        cv2.destroyAllWindows()

    def stop(self):
        """
        Sets 'keep_running' to False to stop the running loop if running.
        :return: None
        """
        self.keep_running = False


def main():
    port = PORT
    server_address = SERVER_ADDRESS
    width = RESOLUTION_W
    height = RESOLUTION_H

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server',
                        help='IP Address of the server which you want to connect to, default'
                             ' is ' + SERVER_ADDRESS,
                        required=True)
    parser.add_argument('-p', '--port',
                        help='The port which you want the Streaming Server to use, default'
                             ' is ' + PORT, required=False)
    parser.add_argument(
        '-rw', '--width', help=f'set the window width, default is {width}', required=False)
    parser.add_argument(
        '-rh', '--height', help=f'set the window height, default is {height}', required=False)

    args = parser.parse_args()

    if args.port:
        port = args.port
    if args.server:
        server_address = args.server
    if args.width:
        width = int(args.width)
    if args.height:
        height = int(args.height)

    streamer = Streamer(server_address, port, width, height)
    streamer.start()


if __name__ == '__main__':
    main()
