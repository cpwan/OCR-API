from flask import Flask, request, jsonify
import base64
import subprocess
import uuid
import os
from functools import lru_cache
app = Flask(__name__)
def getRandomID(length=8):
    return uuid.uuid4().hex[:length]

@app.route('/image-sync', methods=['POST'])
def sync_ocr():
    data = request.get_json(force=True)
    bytes_base64 = data['image_data'].encode()
    image_data = base64.b64decode(bytes_base64)
    ID=getRandomID()
    pathToImages=os.path.join('images',ID)
    open(pathToImages, 'wb').write(image_data)
    command = ['tesseract', pathToImages, 'stdout', '--psm', '1', '--oem', '1', 'quiet']
    process = subprocess.run(command, stdout=subprocess.PIPE)
    text=process.stdout.decode('utf-8')
    out=jsonify({'text':text})
    return out


class TaskManager:
    def __init__(self):
        self.tasks={}

    def create(self,ID,item):
        self.tasks[ID]=item

    def find_finished(self,ID):
        if ID in self.tasks and self.tasks[ID].poll()==0:
            return True
        return False

    def get(self, ID):
        process = self.tasks.pop(ID)
        out = process.communicate()[0].decode('utf-8')
        return out

    # # alternative version to cached the result
    # @lru_cache(maxsize=None)
    # def get(self, ID):
    #     process = self.tasks[ID]
    #     out = process.communicate()[0].decode('utf-8')
    #     return out

taskManager=TaskManager()

@app.route('/image', methods=['POST'])
def async_ocr_post():
    data = request.get_json(force=True)
    bytes_base64 = data['image_data'].encode()
    image_data = base64.b64decode(bytes_base64)
    ID = getRandomID()
    pathToImages=os.path.join('images',ID)
    open(pathToImages, 'wb').write(image_data)
    command = ['tesseract', pathToImages, 'stdout', '--psm', '1', '--oem', '1', 'quiet']
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    taskManager.create(ID,process)
    out=jsonify({'task_id':ID})
    return out

@app.route('/image', methods=['GET'])
def async_ocr_get():
    data = request.get_json(force=True)
    ID = data['task_id']

    text=None
    if taskManager.find_finished(ID):
        text=taskManager.get(ID)

    out = jsonify({'task_id': text})
    return out

