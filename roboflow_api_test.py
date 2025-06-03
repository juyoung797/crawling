import os
from roboflow import Roboflow


roboflow_api_key=os.getenv("ROBOFLOW_API_KEY")
workspate_name = "cafesegmentation"
project_name = "window-detection-avt6g"
model_version = 2

rf = Roboflow(api_key=roboflow_api_key)
project = rf.workspace(workspate_name).project(project_name) 
model = project.version(model_version).model  # 버전 번호: "1"

# 예측
image_path = r"dataset\images\test\ins_0016.jpg"
prediction = model.predict(image_path, confidence=40, overlap=30).json()

# 결과 확인
print(prediction)

# 예측 결과가 그려진 이미지 저장
model.predict(image_path).save("dataset/images/test/ins_0016_predicted.jpg")