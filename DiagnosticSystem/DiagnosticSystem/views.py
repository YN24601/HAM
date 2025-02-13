from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from .mixins import LoginRequiredMixin
import os
from django.conf import settings

import torch
import torchvision.models as models
from torchvision import transforms
import torch.nn.functional as F
from PIL import Image
from django.conf import settings

class HomeView(TemplateView):
    template_name = 'home.html'
    
class DiseaseView(TemplateView):
# class DiseaseView(LoginRequiredMixin, TemplateView):
    template_name = 'disease_intro.html'
    # def get(self, request, *args, **kwargs):
    #     if request.is_ajax():
    #         return JsonResponse({'status': 'authenticated'})
    #     return super().get(request, *args, **kwargs)


class ClassificationView(TemplateView):
    template_name = 'classification.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            upload_file = request.FILES['image']
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            file_path = os.path.join(settings.MEDIA_ROOT, upload_file.name)
            with open(file_path, 'wb') as f:
                for chunk in upload_file.chunks():
                    f.write(chunk)

            try:
                # 加载模型
                model = models.mobilenet_v2(pretrained=False)
                num_classes = 7  # 七分类
                model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, num_classes)
                model.load_state_dict(torch.load('model/mobilenetv2_model.pth', map_location=torch.device('cpu')))
                model.eval()

                # 定义预处理步骤
                preprocess = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])

                # 加载图像
                image = Image.open(file_path)
                input_tensor = preprocess(image)
                input_batch = input_tensor.unsqueeze(0)  # 添加batch维度

                # 使用CPU进行预测
                device = torch.device("cpu")
                model.to(device)
                input_batch = input_batch.to(device)

                # 预测
                with torch.no_grad():
                    output = model(input_batch)
# 计算概率
                probabilities = F.softmax(output, dim=1)[0]  # 获取概率分布
                top_probabilities, top_indices = torch.topk(probabilities, 3)  # 获取前3个概率及其索引

                # 类别名称
                class_names = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

                # 构建预测结果
                top_predictions = []
                for i in range(3):
                    class_name = class_names[top_indices[i].item()]
                    probability = top_probabilities[i].item() * 100  # 转换为百分比
                    top_predictions.append({
                        'class_name': class_name,
                        'probability': round(probability, 2)  # 保留两位小数
                    })

                # 返回预测结果
                return render(request, 'classification.html', {'top_predictions': top_predictions})

            except Exception as e:
                return render(request, 'classification.html', {
                    'error': f"无法处理文件，请确认您上传了正确的文件类型。错误信息：{str(e)}"
                })

        return render(request, 'classification.html')
