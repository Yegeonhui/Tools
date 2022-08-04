# Background Augmentation
> 원활한 모델 학습을 위해 성게, 불가사리가 여러 배경에 있어야 된다.

## How to use?
1. 객체별로 추출된 사진, 배경만 추출된 사진 구축
2. 객체 사진 중 한장을 랜덤으로 가지고와서
3. 배경만 있는 이미지에서 랜덤포인트로 붙이기
4. 정보를 xml파일에 저장

## install Library
```
pip install opencv-python
pip install numpy
pip install elementpath
pip install glob2
```
