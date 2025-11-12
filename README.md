# Gesture Clicking and Draging

Python Based Application. Tracks hand gestures to click or drag your mouse on the screen.
## Logic and Usage

Uses OpenCV for Camera display and drawing the hand skeleton on the display.\
Uses Mediapipe to track the hands and gestures.\
Uses PyAutoGUI for interpreting the gestures as input on the computer.\
\
Left hand is used for mouse control, you need to have your middle and index finger together to move the mouse.\
Right hand is used for mouse clicks, pinch your index and thumb to click, but if you have your middle finger close to your index finger when you pinch, it will be detected as dragging.
## Installation

Install the required libraries on your environment.

```bash
  pip install opencv-python mediapipe pyautogui numpy
```

This project was made possible by the following open-source technologies.
Make sure you install the correct versions of each component.

### Core Components
| Component | Version |
| :--- | :--- |
| [Python](https://www.python.org/) | `3.10.9` |
| [OpenCV](https://pypi.org/project/opencv-python/) | `4.12.0.88` |
| [MediaPipe](https://pypi.org/project/mediapipe/) | `0.10.14` |
| [NumPy](https://pypi.org/project/numpy/) | `2.2.6` |
| [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) | `0.9.54` |


### References

*   The computer vision implementation was heavily inspired by the [Viral Monkey Thinking Meme Project](https://github.com/K4ZED/MonkeyMeme-Gesture_Tracker/tree/main) created by [Kenza Athallah Nandana Wijaya](https://github.com/K4ZED). A big thank you to him.
