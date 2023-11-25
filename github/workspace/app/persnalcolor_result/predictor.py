import os
import pandas as pd
import librosa
import torch
import torchvision
from torchvision import datasets, transforms, models
import numpy as np
import torch.nn as nn
import torch.optim as optim
from PIL import Image
import matplotlib.pyplot as plt
import librosa.display

# load model
model_dir = os.path.dirname(os.path.abspath(__file__))
load_path = os.path.join(model_dir, 'learning_model', 'DenseNet121_img_aihub_pretrained.pth')
load_weights = torch.load(load_path, map_location={'cuda:0': 'cpu'})
model = torchvision.models.densenet121(pretrained=True)
model.classifier = nn.Linear(in_features=1024, out_features=4)
model.eval()
model.load_state_dict(load_weights)

# Preprocessing wavfile
class Testwav():
    def __init__(self, file, frame_length=0.025, frame_stride=0.010):
        self.file = file
        self.frame_length = frame_length
        self.frame_stride = frame_stride
    
    def __getitem__(self):
        X, sample_rate = librosa.load(self.file, res_type='kaiser_fast', sr=16000, offset=0.0)
        input_nfft = int(round(sample_rate * self.frame_length))
        input_stride = int(round(sample_rate * self.frame_stride))

        S = librosa.feature.melspectrogram(y=X, n_mels=64, n_fft=input_nfft, hop_length=input_stride)
        P = librosa.power_to_db(S, ref=np.max)

        return P

def getimg(data):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    librosa.display.specshow(data, ax=ax, sr=16000, hop_length=int(round(16000*0.025)), x_axis='time', y_axis='linear')
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig('predict.jpg', bbox_inches=extent)
    img_path = 'predict.jpg'
    plt.ioff()
    plt.close()
    return img_path

test_transforms = transforms.Compose([transforms.Resize(255),
                                      transforms.CenterCrop(224),
                                      transforms.ToTensor(),
                                      transforms.Normalize([0.485, 0.456, 0.406],
                                                           [0.229, 0.224, 0.225])])

class img2tensor():
    def __init__(self, data_path, transforms=test_transforms):
        self.data_path = getimg(Testwav(data_path).__getitem__())
        self.transforms = transforms
        
    def __getitem__(self):
        image = Image.open(self.data_path)
        return test_transforms(image)

class Predictor(object):
    def __init__(self, model, device='cpu'):
        self.model = model
        self.cls_name = {0:'angry', 1:'neutral', 2:'sad', 3:'happy'}
        self.device = device

    def predict(self, audio):
        audio_info = img2tensor(audio).__getitem__().unsqueeze(0)
        outputs = self.model(audio_info)
        probability = torch.softmax(outputs, 1)
        probability = probability.squeeze()
        proba, idx = torch.max(probability, dim=0)
        emo_proba = proba.item()
        idx = idx.item()
        emo_label = self.cls_name[idx]
        return emo_label
