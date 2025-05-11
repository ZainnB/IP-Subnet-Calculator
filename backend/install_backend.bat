@echo off
echo Installing backend dependencies...
python -m pip install --upgrade pip
pip install fastapi uvicorn pandas
echo All packages installed successfully!
pause

