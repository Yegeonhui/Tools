# Stitching
> 여러장의 이미지를 하나로 합치는 코드

## What is Stitching?
1. 동일 장면의 사진을 자연스럽게 붙여서 한장의 사진으로 만드는 기술이다.
2. 기본적인 방법은 여러장의 영상에서 특징점을 검출하고 특징점이 동일한 것들을 찾아서 두 장의 영상과의 투시변환 관계를 찾아내어 이어붙인다.

## How to use?
1. step1_CameraCalibration.py
- 카메라의 왜곡을 펴주는 코드 
2. step2_Stitching.py
- 왜곡이 없어진 이미지를 합쳐주는 코드

## install Library
```
pip install opencv-python
pip install glob2
pip install numpy
```
