import torch
import torch.nn as nn
from flask import Flask
from flask import request
from PIL import Image
from io import BytesIO
from models import CNN
from torchvision.transforms import Compose, ToTensor, Resize
from collections import OrderedDict
# import matplotlib.pyplot as plot
app = Flask(__name__)
 
model_path = '/home/VerificationDemo/checkpoints/model.pth'
source = [str(i) for i in range(0, 10)]
source += [chr(i) for i in range(97, 97+26)]
alphabet = ''.join(source)

@app.route('/api/predict', methods=['POST'])
def post_predict():
  text="failure"
  if request.method == 'POST':
    file = request.get_data()
    img = Image.open(BytesIO(file)).convert('RGB')
    print('宽：%d,高：%d'%(img.size[0],img.size[1]))
    width=img.size[0]
    height=img.size[1]
    transform = Compose([Resize(height, width), ToTensor()])
    img = transform(img)
    cnn = CNN()
    if torch.cuda.is_available():
        cnn = cnn.cuda()
    cnn.eval()
    cnn.load_state_dict(torch.load(model_path,map_location='cpu'))
    img = img.view(1, 3, height, width).cuda()
    output = cnn(img)
    output = output.view(-1, 36)
    output = nn.functional.softmax(output, dim=1)
    output = torch.argmax(output, dim=1)
    output = output.view(-1, 4)[0]
    text=''.join([alphabet[i] for i in output.cpu().numpy()])
    # print('pred: '+text)
    # plot.imshow(img.permute((0, 2, 3, 1))[0].cpu().numpy())
    # plot.show()

  return text

@app.route('/api/values')
def index():
  return "Hello, World!"
 
if __name__ == '__main__':
  app.run(host='127.0.0.1',port='5000')

  