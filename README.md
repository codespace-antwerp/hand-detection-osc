# Hand Detection

This project uses hand detection by [MediaPipe](https://google.github.io/mediapipe/) to detect hands in a video stream, select the wrist position, and then send that information over OSC.

This can be used to control Ableton Live, for example, to influence the music based on the amount of hands, or the position of the hands.

## Setup in Python

Install the requirements:

```bash
pip install -r mediapipe python-osc
```

## Setup in Ableton

We suggest installing [LiveGrabber](https://www.showsync.com/tools#livegrabber):

- Install the GrabberReceiver and ParamGrabber devices by placing in your Live project folder (i.e. next to "rebuild_from_scratch_osc_new_range.als" ). I've included them as attachments.
- In Ableton, look for Places>Current Project to find the devices.
- Each track needs a GrabberReceiver device configured to port 8000. You should see the events streaming in.
- For the mapping you'll want a ParamGrabber. The ParamGrabber needs to be immediately right of the device you want to control. You can configure the parameter using the learn button, and the address you can type in, or choose from the recent event list (this doesn't always work).

## Checking the signal

I've included `osc_sniffer.py`, to check the OSC signal. You can run it with:

```bash
python osc_sniffer.py
```