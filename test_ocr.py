import os
import tempfile
from flask import request, jsonify
import pytest
import json
import app
from getTestPair import *

@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client

image_data,expected_text,= getTestPairs('photo.tif')

def test_sync(client):
    rv = client.post('/image-sync', json={"image_data": image_data})
    rv_json=json.loads(rv.get_data(as_text=True))
    expected={"text":expected_text}
    assert rv_json==expected

def test_async(client):
    rv = client.post('/image', json={"image_data": image_data})
    rv_json=json.loads(rv.get_data(as_text=True))
    assert 'task_id' in rv_json
    task_id = rv_json['task_id']
    while True:
        rv2 = client.get('/image', json={"task_id": task_id})
        rv_json2 = json.loads(rv2.get_data(as_text=True))
        if rv_json2["task_id"]!=None:
            break
    expected={"task_id":expected_text}
    assert rv_json2==expected


