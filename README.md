# Gym Analyse

**Real-time exercise recognition, repetition counting, and form feedback from webcam video.**

Gym Analyse is an academic project that combines computer vision and machine learning to analyze basic workout movements. The app extracts pose landmarks from a webcam feed, classifies the movement, counts repetitions, and provides squat-form feedback. A Streamlit interface lets users control a session and review saved workout history.

## Features

- Pose estimation and landmark feature extraction with MediaPipe and OpenCV
- Sequence classification for squats, pushups, pullups, and idle movement
- Repetition counting with movement-cycle logic
- Squat-form feedback based on pose angles
- Session summaries with locally saved history
- Session totals, repetition trends, and CSV export

## Architecture

![Gym exercise analysis architecture](Black%20and%20white%20arch.png)

OpenCV captures webcam frames, MediaPipe estimates pose landmarks, and the feature extractor prepares them for the trained bidirectional LSTM classifier. Predictions feed repetition counting and squat-form analysis. Streamlit displays live results and session summaries; saved sessions are read by the analytics tab.

## Screenshots

### Workout Session Screen

![AI Fitness Trainer session screen](screenshots/session.png)

### Session History Screen

![AI Fitness Trainer data screen](screenshots/data.png)

## Technology Stack

- Python 3.10
- TensorFlow/Keras for sequence classification
- MediaPipe and OpenCV for pose estimation and video capture
- Streamlit for the application interface
- NumPy, pandas, and scikit-learn for feature and data processing

## Getting Started

### Prerequisites

- Python 3.10
- A connected webcam for live exercise analysis
- Local model files, described below

### Install

On Windows, run the included setup script, which creates `minorenv` and installs the project dependencies:

```bat
setup.bat
```

Or install manually in a virtual environment:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On macOS or Linux, create and activate the environment with `python3.10 -m venv .venv` and `source .venv/bin/activate`, then install `requirements.txt`.

### Model Files

Trained model files are not included in this repository. Before starting the app, place both of these files in a local `model/` directory:

```text
model/exercise_model.h5
model/scaler.pkl
```

To train a model instead, provide the training arrays `X.npy`, `y.npy`, `train_idx.npy`, and `test_idx.npy` in the project root, create the output directory with `mkdir model`, and run:

```bash
python train_model.py
```

The training script saves the model and scaler under `model/`. Datasets and generated model files are intentionally excluded from Git.

## Usage

From the project directory, start the app:

```
streamlit run app.py
```

The app opens in a browser. Use **Start** to begin webcam analysis, **Stop** to finish and review a session summary, and **Cancel** to discard the current session. Saved sessions appear in the **Data** tab and are stored locally in `sessions.csv`.

## Project Structure

- `app.py`: Streamlit interface and webcam session flow
- `feature_extractor.py`: Pose landmark features and joint angles
- `classifier.py`: Model loading, prediction, and output filtering
- `rep_counter.py`: Repetition state and cycle counting
- `form_analyzer.py`: Squat-form feedback
- `pose_draw.py`: Pose overlay rendering
- `session_manager.py`: Session utilities and workout-log persistence
- `analytics.py`: Workout analytics utilities
- `train_model.py`: Bidirectional LSTM training pipeline
- `screenshots/`: README screenshots

## Data and Limitations

Workout history, datasets, and trained model artifacts stay local and are excluded from Git. Session history is written to `sessions.csv` in the working directory. The current form-feedback implementation analyzes squats; exercise recognition and rep counts depend on the locally supplied model and training data. This project is an academic prototype, not a medical or professional coaching tool.

## Requirements

Dependencies are listed in [`requirements.txt`](requirements.txt).

## License

This academic project is available under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

For usage questions or extension ideas, contact [@HarshavardhanKakarla](https://github.com/HarshavardhanKakarla) or [open an issue](https://github.com/HarshavardhanKakarla/Fitness-Monitoring/issues).