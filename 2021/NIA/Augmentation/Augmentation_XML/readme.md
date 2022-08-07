# Augmentation_XML
> Nia 사업간 모델학습을 위해 XML, image를 증강하는 코드

## How to use?
1. XML 내부에 객체가 5개 이상인 경우만 Augmentation 수행
2. crop_h, crop_w만큼 이미지를 자르고, XML도 똑같이 자름
3. 자른 이미지내에 있는 객체가 criteria 보다 큰 경우를 카운트
4. 3번을 만족하는 객체가 min_object 보다 많은 경우 이미지를 저장

## install Library
```
pip install opencv-python
pip install elementpath
pip install numpy
pip install pillow
pip install piexif
```
