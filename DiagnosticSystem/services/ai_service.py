# services/ai_service.py
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import os

class AISkinDiagnosisService:
    def __init__(self, model_path='model/shufflenet_final.pth'):
        self.model = None
        self.preprocess = None
        self.class_names = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']
        self.model_path = model_path
        self._load_model()
    
    def _load_model(self):
        """加载预训练的ShuffleNetV2模型"""
        # 初始化ShuffleNetV2_x1_0结构
        self.model = models.shufflenet_v2_x1_0(pretrained=False)
        num_classes = 7
        
        # 替换全连接层 7类
        in_features = self.model.fc.in_features
        self.model.fc = nn.Linear(in_features, num_classes)
        
        # 加载训练好的权重
        self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))
        self.model.eval()
        
        # 预处理保持与MobileNetV2相同
        self.preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def predict_image(self, image_path):
        """对图像进行预测"""
        try:
            image = Image.open(image_path)
            input_tensor = self.preprocess(image)
            input_batch = input_tensor.unsqueeze(0)
            
            device = torch.device("cpu")
            self.model.to(device)
            input_batch = input_batch.to(device)
            
            with torch.no_grad():
                output = self.model(input_batch)
            
            probabilities = F.softmax(output, dim=1)[0]
            top_probabilities, top_indices = torch.topk(probabilities, 3)
            
            top_predictions = []
            for i in range(3):
                class_name = self.class_names[top_indices[i].item()]
                probability = top_probabilities[i].item() * 100
                top_predictions.append({
                    'class_name': class_name,
                    'probability': round(probability, 2)
                })
            
            return {
                'ai_diagnosis': top_predictions[0]['class_name'],
                'top_predictions': top_predictions
            }
        except Exception as e:
            raise Exception(f"预测失败: {str(e)}")