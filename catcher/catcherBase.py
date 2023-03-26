import requests
import time
from urllib.parse import urljoin
import lxml.html

class CatcherBase:

    # URL = "{default url}"

    def __init__(self, url=None, session=None):
        #todo: check

        self.firstUrl = url if url else self.URL
        self.session = session if session is not None else requests.Session()
        self._course = None


    @property
    def courses(self, ) -> list[dict]:
        """
        property 取得課程資訊快取並
        """
        if self._course is None:
            self._course = self.getCourses()
        return self._course


    def getCourses(self, ) -> list:
        """
        輸出所有課程資訊
        """
        return list( self.iterCourses() )


    def iterCourses(self, ):
        """
        迭代輸出 Course information
        此方法是 getCourses 迭代版本，惰性的抓取網路資訊
        """
        raise RuntimeError("這是一個抽象方法，不應被調用")


    def _getHtmlTree(self, url, tryCount=3, delay=1):
        return getHtmlTree(url, self.session, tryCount, delay)


class DoublePageCatcherBase(CatcherBase):

    # URL: str

    def iterCourses(self, ):
        """
        迭代輸出 Course information
        此方法是 getCourses 迭代版本，惰性的抓取網路資訊
        """
        for page in self._iterPages():
            for info in self._getPageCourses(page):
                yield info


    def _iterPages(self, ):
        """
        迭代目錄頁的 lxml 物件
        """
        yield ( page:= self._getHtmlTree(self.firstUrl) )
        while nextUrl:= self._parseNextPageUrl(page):
            yield ( page:= self._getHtmlTree(nextUrl) )


    def _parseNextPageUrl(self, element) -> str:
        """
        取得目錄下一頁的 url ，不存在則回傳 None
        """
        assert isinstance(element, lxml.etree._Element)
        if urls:= element.xpath(self.XPATH["nextUrl"]):
            return urljoin(element.base_url, urls[0])
        return None


    def _getPageCourses(self, page) -> list:
        """
        回傳 page 中的課程資訊
        """
        courses = []
        for info in self._parsePage(page)["courses"]:
            courses.append( self._catchCourseInfo(info) )

        return courses


    def _catchCourseInfo(self, simpleInfo: dict) -> dict:
        """
        獲取課程詳細資訊
        """
        raise RuntimeError("這是一個抽象方法，不應被調用")


    def _parsePage(self, page) -> dict:
        """
        解析 page 資訊
        """
        raise RuntimeError("這是一個抽象方法，不應被調用")


class MultiPageCatcher(DoublePageCatcherBase):

    def _iterPages(self, startUrl=None):
        """
        迭代目錄頁的 lxml 物件
        """
        if startUrl is None:
            startUrl = self.firstUrl
        page = self._getHtmlTree(startUrl)

        info = self._parsePage(page)
        if self._isCategoryPage(page):
            for categorityInfo in info["categories"]:
                yield from self._iterPages(categorityInfo["url"])

        else:
            yield page
            while nextUrl:= self._parseNextPageUrl(page):
                yield ( page:= self._getHtmlTree(nextUrl) )


class SinglePageCatcher(CatcherBase):

    #URL: str

    def iterCourses(self, ):
        """
        迭代輸出 Course information
        此方法是 getCourses 迭代版本，惰性的抓取網路資訊
        """
        page = self._getHtmlTree(self.firstUrl)
        for courseInfo in self._parsePage(page)["courses"]:
            yield self._catchCourseInfo(courseInfo)


    def _parsePage(self, page) -> dict:
        """
        解析 page 資訊
        """
        raise RuntimeError("這是一個抽象方法，不應被調用")


    def _catchCourseInfo(self, simpleInfo) -> dict:
        """
        獲取課程詳細資訊
        """
        raise RuntimeError("這是一個抽象方法，不應被調用")


def firstDefault(sequence, default=None):
    assert hasattr(sequence, "__getitem__")
    return sequence[0] if sequence else default


def createHtmlTree(content, base_url):
    tree = lxml.html.fromstring(content, base_url=base_url)
    return tree


def getHtmlTree(url, session=requests.Session(), tryCount=3, delay=1):

    errors = []
    for i in range(tryCount):

        try:
            return createHtmlTree(session.get(url).content, url)

        except requests.Timeout as exc:
            errors.append(exc)
            time.sleep(delay)

    raise requests.Timeout("重複超時", errors)

