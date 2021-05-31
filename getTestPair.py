import base64
import subprocess

def getTestPairs(filename):
    file = open(filename, 'rb')
    encoded_string = base64.b64encode(file.read())
    text_base64 = encoded_string.decode('utf-8')
    command = ['tesseract', filename, 'stdout', '--psm', '1', '--oem', '1', 'quiet']
    process = subprocess.run(command, stdout=subprocess.PIPE)
    expected_text=process.stdout.decode('utf-8')

    return text_base64,expected_text

if __name__=='__main__':
    text_base64,expected_text,= getTestPairs('photo.tif')
    print(text_base64)
    print(repr(expected_text))
