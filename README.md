# ✋ Gesture-Controlled YouTube Interface 🎮

Control your YouTube playback using **just your hand gestures**!
This project uses **MediaPipe**, **OpenCV**, and **PyAutoGUI** to detect hand signs via your webcam and simulate keyboard controls like play, pause, volume, and more.

---

## 🧠 Features

| Gesture         | Action        |
| --------------- | ------------- |
| ✋ Palm          | Play / Pause  |
| ✊ Fist          | Mute / Unmute |
| 👍 Thumbs Up    | Volume Up     |
| 👎 Thumbs Down  | Volume Down   |
| 🖐 Index Finger | Seek Forward  |
| ✌ Peace Sign    | Seek Backward |
| 🤟 Rock Sign    | Next Song     |

> Make sure your webcam is enabled and you're using good lighting for accurate recognition.

---

## 🛠 Tech Stack

* 🧠 [MediaPipe](https://google.github.io/mediapipe/) – Real-time hand detection
* 🎥 OpenCV – Video frame processing
* ⌨️ PyAutoGUI – Triggering keyboard commands
* 🐍 Python 3.8+



## 🚀 Usage

Make sure your browser is focused on YouTube.

```bash
python gesture_control.py


📌 **To exit the program**, press the `e` key.


## 📂 Project Structure

```
Gesture-Control-YouTube/
│
├— gesture_control.py      # Main Python script
├— requirements.txt        # List of dependencies
└— README.md               # You're reading this!
```

---

## 📸 How It Works (Architecture)

 Webcam Feed
     ↓
 OpenCV → Frame Preprocessing
     ↓
MediaPipe Hands → Extract Landmarks
     ↓
Gesture Logic → Interpret Finger Patterns
     ↓
PyAutoGUI → Trigger Keyboard Commands (like 'space', 'm', 'volumeup', etc.)
```

---

## 🥮 Tips for Accuracy

* Use consistent **lighting**.
* Keep your **hand centered** in the webcam.
* Keep only **one hand visible**.
* Keep your hand at a reasonable **distance from the camera**.


## ⚠️ Disclaimer

This is a fun, educational project and may not work perfectly across all devices or hand types.
Always test in your own environment and feel free to improve the logic!

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 🤝 Acknowledgements

* [MediaPipe by Google](https://google.github.io/mediapipe/)
* [OpenCV](https://opencv.org/)
* [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)

---

### 🔗 Author

**Venkata Sai Tarun Varma**
📍 Andhra Pradesh, India
👨‍💻 [GitHub](https://github.com/Tarunvarma07).E-mail:varmachintha30@gmail.com
