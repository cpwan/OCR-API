# OCR
## About
The code serves the API for OCR.
The program accepts two endpoints: `image-sync` and `image`.
### Synchronous inference
The `image-sync` ednpoint receives base64 images 
```
curl -POST "http://localhost:5000/image-sync" -d '{"image_data": "<b64 encoded image>"}'
```
and return a json response
```
{
"text": "<recognized text>"
}
```
### Asynchronous inference
The `image` ednpoint receives base64 images for POST requests
```
curl -POST "http://localhost:5000/image" -d '{"image_data": "<b64 encoded image>"}'
```
and return a json response
```
{
"task_id": "<task id>"
}
```

After that, the results of the inference can be retrieved with GET request on the `image` ednpoint
```
curl -GET "http://localhost:5000/image" -d '{"task_id": "<task id>"}'
```
and return a json response if the inference is done
```
{
"task_id": "<recognized text>"
}
```
otherwise, return None
```
{
"task_id": null
}
```


## Dependency
- python 3.8
- Flask

## Build
Option 1. Docker
``docker-compose -f docker-compose.dev.yml up --build``

Option 2. Manually install depedencies
```
apt-get update && apt-get install -y tesseract-ocr-eng
pip3 install -r requirements.txt
python3 -m flask run --host=0.0.0.0
```


