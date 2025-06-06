import torch
import clip
from PIL import Image

# 디바이스 설정 (GPU 사용 가능 시 CUDA 사용)
device = "cuda" if torch.cuda.is_available() else "cpu"

# 모델과 전처리기 로드
model, preprocess = clip.load("ViT-B/32", device=device)

# 테스트 이미지 불러오기
image = preprocess(Image.open("dataset/images/train/ins_0027.jpg")).unsqueeze(0).to(device)

# 텍스트 라벨 정의
labels = [
    "a photo of a mountain",
    "a photo of the sea",
    "a photo of a forest",
    "a photo of a lake"
]

text = clip.tokenize(labels).to(device)

# 이미지-텍스트 유사도 계산
with torch.no_grad():
    logits_per_image, _ = model(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

# 결과 출력
for label, prob in zip(labels, probs[0]):
    print(f"{label}: {prob*100:.2f}%")
