import argparse

import cv2
import numpy as np
import zmq

from constants import PORT
from utils import string_to_image


class StreamViewer:
    def __init__(self, port=PORT, display=True):
        """
        Binds the computer to a ip address and starts listening for incoming streams.

        :param port: Port which is used for streaming
        """
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.SUB)
        self.footage_socket.bind('tcp://*:' + port)
        self.footage_socket.setsockopt_string(
            zmq.SUBSCRIBE, np.compat.unicode(''))
        self.current_frame = None
        self.keep_running = True
        self.display = display

    def receive_stream(self):
        """
        Displays displayed stream in a window if no arguments are passed.
        Keeps updating the 'current_frame' attribute with the most recent frame, this can be accessed using 'self.current_frame'
        :param display: boolean, If False no stream output will be displayed.
        :return: None
        """
        self.keep_running = True
        while self.footage_socket and self.keep_running:
            try:
                frame = self.footage_socket.recv_string()
                self.current_frame = string_to_image(frame)

                if self.display:
                    cv2.imshow("Stream", self.current_frame)
                    cv2.waitKey(1)

            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break
        print("Streaming Stopped!")

    def stop(self):
        """
        Sets 'keep_running' to False to stop the running loop if running.
        :return: None
        """
        self.keep_running = False


def main():
    port = PORT
    display = 'yes'

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',
                        help='The port which you want the Streaming Viewer to use, default'
                             ' is ' + PORT, required=False)
    parser.add_argument('-d', '--display',
                        help=f'Display into window? yes or no, default is {display}', required=False)

    args = parser.parse_args()
    if args.port:
        port = args.port

    if args.display and args.display.lower() == 'yes':
        display = True
    elif args.display and args.display.lower() == 'no':
        display = False

    stream_viewer = StreamViewer(port, display)
    stream_viewer.receive_stream()


if __name__ == '__main__':
    main()
