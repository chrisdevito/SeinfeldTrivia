echo Building venv...
python -m venv ./venv

call .\venv\Scripts\activate.bat

echo Installing requirements...
pip install -r .\requirements.txt
pause
