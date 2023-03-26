# Tw-open-course-catcher
一隻能夠爬取台灣各大學開放式課程的爬蟲

# 特色
- 支持台大、清華、交大開放式課程抓取
- 抓取的內容細緻，包括個章節與課程影片連結

# 安裝
```shell
# copy project
git clone https://github.com/u-tung/Tw-course-catcher

# install packages
cd Tw-course-catcher
pip install -r requirements.txt
```

# 使用範例
- 運行時依據網路環境與開放式課程平台伺服器回應時間不等，可能執行時間較久(4-5小時)，請耐心等候
```python
import json
from catcher.catcherBase import CatcherBase
from catcher.ntuCatcher import NtuCatcher
from catcher.nthuCatcher import NthuCatcher
from catcher.nycuCatcher import NycuCatcher

def coursesDump(catcher, filename):

    assert issubclass(catcher, CatcherBase)
    nc = catcher()

    try:
        courses = []
        for info in nc.iterCourses():
            print(f"{info['title']}")
            courses.append(info)

    finally:
        print("輸出 json...")
        with open(filename, "w") as file:
            json.dump(courses, file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    coursesDump(NycuCatcher, "nycuCourses.json")
    coursesDump(NthuCatcher, "nthuCourses.json")
    coursesDump(NtuCatcher, "ntuCourses.json")
```

## 輸出範例
```json
[
    {
        "category": "http://ocw.nctu.edu.tw/course_detail.php?bgid=28&gid=0&nid=671&page=1",
        "description": "本課程由本校  所提供。\r\n\t \r\n\t本課程由本校  所提供。",
        "teacher": "跨領域設計科學研究中心副主任 曾聖凱老師；人文社會學院兼任講師 詹國禎老師",
        "title": "基礎設計建模與實作 Basic Design Modeling and Fabrication",
        "units": [
            {
                "title": "歡迎光臨新手村－帶你瀏覽3D建模世界的面貌",
                "videoUrl": "https://www.youtube.com/embed/Won_tGIVrEQ"
            },
            {
                "title": "繪製魔法練成陣—草圖繪製是創造的第一步 (Fusion 360 - Sketch)",
                "videoUrl": "https://www.youtube.com/embed/2apWE4lsPaU"
            },
            {
                "title": "創造第一把武器 (Fusion 360 - Extrude)",
                "videoUrl": "https://www.youtube.com/embed/UaAkphWW8Ys"
            },
            {
                "title": "找個瓶子裝補藥 (Fusion 360 - Revolve)",
                "videoUrl": "https://www.youtube.com/embed/WK-sGw62MB0"
            },
            {
                "title": "入手強化首飾 (Fusion 360 - Sweep)",
                "videoUrl": "https://www.youtube.com/embed/heCw9WjQSEU"
            },
            {
                "title": "沒有防具怎麼行 (Fusion 360 - Loft)",
                "videoUrl": "https://www.youtube.com/embed/OEKqYYY6LWw"
            },
            {
                "title": "把瓶子鎖緊補藥才不會漏 (Fusion 360 - Coil)",
                "videoUrl": "https://www.youtube.com/embed/edUJypFjftI"
            },
            {
                "title": "讓裝備變豪華吧！",
                "videoUrl": "https://www.youtube.com/embed/yKzQXbV1wSM"
            }
        ],
        "url": "http://ocw.nctu.edu.tw/course_detail.php?bgid=28&gid=0&nid=671&page=1"
    },
    {
        "category": "http://ocw.nctu.edu.tw/course_detail.php?bgid=28&gid=0&nid=668&page=1",
        "description": "",
        "teacher": "應用數學系 陳暐捷同學",
        "title": "微積分基礎課程 Pre- Calculus",
        "units": [
            {
                "title": "第一章：邏輯",
                "videoUrl": "https://www.youtube.com/embed/1JwJVtTvUCM"
            },
            {
                "title": "第二章：數系",
                "videoUrl": "https://www.youtube.com/embed/7iOxnMWKzMU"
            },
            {
                "title": "第三章：函數(I)",
                "videoUrl": "https://www.youtube.com/embed/Gc_wQNZPjmA"
            },
            {
                "title": "第四章：函數(II)",
                "videoUrl": "https://www.youtube.com/embed/41OHHbpGZeM"
            },
            {
                "title": "第五章：多項式(I)",
                "videoUrl": "https://www.youtube.com/embed/J-ITpWZoErc"
            },
            {
                "title": "第六章：多項式(II)",
                "videoUrl": "https://www.youtube.com/embed/K3BF1QRCtWE"
            },
            {
                "title": "第八章：指數",
                "videoUrl": "https://www.youtube.com/embed/LUYNm3oe0hk"
            },
            {
                "title": "第九章：對數",
                "videoUrl": "https://www.youtube.com/embed/rB0A3nQ0SYs"
            },
            {
                "title": "第十章：三角函數(I)",
                "videoUrl": "https://www.youtube.com/embed/7mqPtyIRCgQ"
            },
            {
                "title": "第十一章：三角函數(II)",
                "videoUrl": "https://www.youtube.com/embed/jGVAkfZWGlw"
            },
            {
                "title": "第十二章：三角函數(III)",
                "videoUrl": "https://www.youtube.com/embed/AG1LFdDdTMg"
            },
            {
                "title": "第十三章：向量與線性空間(I)",
                "videoUrl": "https://www.youtube.com/embed/MDhzEG1aV4Y"
            },
            {
                "title": "第十四章：圓錐曲線",
                "videoUrl": "https://www.youtube.com/embed/qjGLOkHLk1k"
            }
        ],
        "url": "http://ocw.nctu.edu.tw/course_detail.php?bgid=28&gid=0&nid=668&page=1"
    },
    ...
]
```
