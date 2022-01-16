import torch
import torch.nn as nn
import torch.optim as optim

from src.model.Losses import StyleLoss, ContentLoss
from src.model.Normalization import Normalization

from PIL import Image

import torchvision
import torchvision.transforms as transforms
import torchvision.models as models
import torchvision.utils as utils


class StyleTransfer:

    def __init__(self, style_path, content_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.imsize = 512 if torch.cuda.is_available() else 128
        self.style_img = self.image_loader(style_path)
        self.content_img = self.image_loader(content_path)
        self.input_img = self.content_img.clone()

        self.cnn = models.vgg19(pretrained=True).features.to(self.device).eval()
        self.cnn_norm_mean = torch.tensor([0.485, 0.456, 0.406]).to(self.device)
        self.cnn_norm_std = torch.tensor([0.229, 0.224, 0.225]).to(self.device)

        if self.style_img.size() != self.content_img.size():
            self.style_img = transforms.Resize(self.content_img.size()[2:])(self.style_img)

        self.model, self.style_losses, self.content_losses = self.get_style_model_and_losses()

    def image_loader(self, image_name):
        loader = transforms.Compose([
                                    transforms.Resize(self.imsize),
                                    transforms.ToTensor()])
        image = Image.open(image_name)
        image = loader(image).unsqueeze(0)
        return image.to(self.device, torch.float)

    def get_input_optimizer(self):
        optimizer = optim.LBFGS([self.input_img])
        return optimizer

    def get_style_model_and_losses(self):
        normalization = Normalization(self.cnn_norm_mean, self.cnn_norm_std).to(self.device)

        content_layers = ['conv_4']
        style_layers = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_']

        content_losses = []
        style_losses = []

        model = nn.Sequential(normalization)

        i = 0
        for layer in self.cnn.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = 'conv_{}'.format(i)
            elif isinstance(layer, nn.ReLU):
                name = 'relu_{}'.format(i)
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = 'pool_{}'.format(i)
            else:
                raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))

            model.add_module(name, layer)

            if name in content_layers:
                target = model(self.content_img).detach()
                content_loss = ContentLoss(target)
                model.add_module('content_loss_{}'.format(i), content_loss)
                content_losses.append(content_loss)

            if name in style_layers:
                target_feature = model(self.style_img).detach()
                style_loss = StyleLoss(target_feature)
                model.add_module('style_loss_{}'.format(i), style_loss)
                style_losses.append(style_loss)

        for i in range(len(model) - 1, -1, -1):
            if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
                break

        model = model[:(i + 1)]

        return model, style_losses, content_losses

    def run_style_transfer(self, num_steps=300, style_weight=1000000, content_weight=1):
        print('Building the style transfer model...')

        self.input_img.requires_grad_(True)
        self.model.requires_grad_(False)

        optimizer = self.get_input_optimizer()

        print('Optimizing...')
        run = [0]
        while run[0] <= num_steps:

            def closure():
                with torch.no_grad():
                    self.input_img.clamp_(0, 1)

                optimizer.zero_grad()
                self.model(self.input_img)
                style_score = 0
                content_score = 0

                for sl in self.style_losses:
                    style_score += sl.loss
                for cl in self.content_losses:
                    content_score += cl.loss

                style_score *= style_weight
                content_score *= content_weight

                loss = style_score + content_score
                loss.backward()

                run[0] += 1
                if run[0] % 50 == 0:
                    print('run {}'.format(run))
                    print('Style loss: {:4f} Content loss: {:4f}'.format(
                        style_score.item(), content_score.item()
                    ))
                    print()

                return style_score + content_score

            optimizer.step(closure)

        with torch.no_grad():
            self.input_img.clamp_(0, 1)

        return self.input_img

    def save_image(self, path='output.jpg'):
        utils.save_image(self.input_img, path)

    def to_pil(self):
        print(self.input_img.shape)
        return torchvision.transforms.functional.to_pil_image(self.input_img.squeeze())