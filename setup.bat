@echo off

echo =====================================
echo Installing AI Fitness Trainer Setup
echo =====================================

REM ---- Check Python 3.10 ----
py -3.10 --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python 3.10 not found.
    echo Install from: https://www.python.org/downloads/release/python-31011/
    pause
    exit
)

REM ---- Create virtual environment ----
echo Creating virtual environment...
py -3.10 -m venv minorenv

REM ---- Activate ----
call minorenv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

REM ---- Install dependencies (ORDER IMPORTANT) ----
echo Installing numpy...
pip install numpy==1.23.5

echo Installing tensorflow...
pip install tensorflow==2.12.0

echo Installing mediapipe...
pip install mediapipe==0.10.20

echo Installing opencv...
pip install opencv-python==4.8.1.78

echo Installing remaining packages...
pip install streamlit==1.29.0 pandas matplotlib scikit-learn tqdm

REM ---- Remove conflicting keras ----
pip uninstall keras -y

echo =====================================
echo Setup Complete
echo =====================================
pause