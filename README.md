# PiCamera Video Stream with Python, OpenCV and zmq

Webcam or PiCamera Streaming over the Network with Python

## Getting Started

This is a Python Application which makes streaming video from webcams over the network access by tcp.

### Prerequisites

1. Webcam or raspberry pi and camera module

### Installing

A step by step series of examples that tell you how to get a development env running

1. Install all the requirements

```
pip install -r requirements.txt
```

2. Start the viewer, on the server. You can opt -d or --display optional to display in window or not with value yes or no

```
python StreamViewer.py -d yes
or
python StreamViewer.py -d no
```

3. On another machine connected to the same network, start the streamer, and enter the IP of the machine running the StreamViewer.

```
ifconfig
```

get the IP address of the raspberry pi and put into the below command. Also optional you can use -w and -h for window resolution of width and height for display

```
python Streamer.py -s 192.168.1.X -rw 640 -rh 480
```

You will see the video being streamed across the network to your Viewer.

## updating the Rasperrypi cupinfo

go to utils.py and add the cpuinfo in `raspi_cpu_info` list

## Running the tests (WebCam Needed)

```
python -m unittest discover .
```

1. `test_camera.py` - Tests if camera can be detected with OpenCV

   `python -m unittest camera.test_camera`

2. `test_local_streaming.py` - Tests Streaming and Viewing silently locally

   `python -m unittest test_local_streaming`

## Built With

- **[OpenCV](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_intro/py_intro.html)** - a library of programming functions mainly aimed at real-time computer vision.
- **[ZeroMQ](http://zeromq.org/bindings:python)** - a high-performance asynchronous messaging library, aimed at use in distributed or concurrent applications.

I have taken help from various tutorials and documents.
Requesting you to feel free to fork and update with more features.
