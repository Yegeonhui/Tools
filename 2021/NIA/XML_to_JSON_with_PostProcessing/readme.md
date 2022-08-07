# XML_to_JSON_with_PostProcessing
> XML을 JSON으로 변환하면서 후처리 하는 코드

## How to use?
1. 대용량 데이터를 처리하다보니, error가 없는 이미지 10000개당 하나의 폴더로 저장
2. 이미지에 해당하는 XML파일이 있는지 check
3. 속성값이 15개인지 check
4. 객체이름에 번호 제거 ex) (11)plastic -> plastic
5. 객체이름 오태깅 체크 
6. 클래스명이 Blur인 부분 Blur 처리
7. 썸네일 용량이 큰이미지 썸네일 삭제 

## install Library
```
pip install elementpath
pip install pillow
pip install piexif
pip install pytest-shutil
```
