import os 

shell=[
'pkg install android-tools -y',
'pkg install python-numpy -y',
'pkg install python-pillow -y',
'pkg install opencv-python -y',
'pkg install tesseract -y',
'pip install pytesseract '
]

for i in shell :
    os.system(i)