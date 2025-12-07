import torch
import numpy as np
from facenet_pytorch import InceptionResnetV1
from torchvision import transforms
from PIL import Image


class FaceEncoder:
    def __init__(self, device='cpu'):
        self.device = device
        # Load pretrained FaceNet model (trained on VGGFace2 dataset)
        self.model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

        # Image preprocessing pipeline
        self.preproc = transforms.Compose([
            transforms.Resize((160, 160)),
            transforms.ToTensor(),
            transforms.Normalize([0.5]*3, [0.5]*3)
        ])

    def embed(self, face_img):
        """
        Takes a face image (numpy or PIL), preprocesses it,
        passes through FaceNet model, returns 512-D embedding vector.
        """

        # If input is numpy array (OpenCV frame), convert BGR -> RGB PIL
        if isinstance(face_img, np.ndarray):
            face_img = Image.fromarray(face_img[:, :, ::-1])

        # Apply preprocessing
        x = self.preproc(face_img).unsqueeze(0).to(self.device)

        # Inference (no gradients needed)
        with torch.no_grad():
            emb = self.model(x).cpu().numpy().squeeze()

        # Normalize embedding (L2 norm)
        emb = emb / np.linalg.norm(emb)

        return emb.astype('float32')
