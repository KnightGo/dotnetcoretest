import json
import requests
import base64
from io import BytesIO
from PIL import Image
from sys import version_info


def base64_api(base64_img):
    b64 = str(base64_img, encoding='utf-8')
    data = {"username": "yw", "password": "UD7MZKHfh4Ab", "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    return result


if __name__ == "__main__":
    img_path = "D:/img/rand/f7cccbeea5bc7d5a4059406c101b10e8.png"
    img = Image.open(img_path)
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    result = base64_api(base64.b64encode(buffered.getvalue()))
    if result['success']:
        print(result["data"]["result"])
    else:
        print(result["message"])

    print(result)
        