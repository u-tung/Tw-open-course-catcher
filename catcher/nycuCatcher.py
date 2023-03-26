from .catcherBase import firstDefault, MultiPageCatcher
import requests
from urllib.parse import urljoin
import lxml.etree

class NycuCatcher(MultiPageCatcher):

    URL = "http://ocw.nctu.edu.tw/course.php"
    XPATH = {
        #"coursesDiv": "//div[contains(@class, 'singleCourse')]",
        "nextUrl": "//i[contains(@class, 'fa-angle-right')]/parent::a/@href"
    }
    DEFAULT_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"

    def __init__(self, url=None, session=None):
        if session is None:
            session = requests.Session()
            session.headers["User-Agent"] = self.DEFAULT_UA
        super().__init__(url, session)


    def _parsePage(self, page):
        return (self._parseCategoryPage, self._parseCatalogPage)[self._isCatalogPage(page)](page)

    
    def _isCatalogPage(self, page):
        return "course_list.php" in page.base_url


    def _isCategoryPage(self, page):
        return not self._isCatalogPage(page) #XXX; 不好的實現


    def _parseCategoryPage(self, categoryPage):

        info = {"categories": [], "type": "category"}
        for div in categoryPage.xpath("//div[contains(@class, 'col-md-3')]"):
            info["categories"].append(
                {
                    "url": urljoin( div.base_url, div.xpath(".//a/@href")[0] ),
                    "title": div.xpath(".//h5/text()")[0].strip()
                })

        return info


    def _parseCatalogPage(self, catalogPage):

        info = {"courses": [], "type": "catalog"}
        for tr in catalogPage.xpath("//table[contains(@class, 'table-bordered')]/tr")[1:]:
            info["courses"].append(
                {
                    "url": urljoin(tr.base_url, tr.xpath(".//a/@href")[0].strip()),
                })

        return info


    def _catchCourseInfo(self, simpleInfo: dict) -> dict:

        element = self._getHtmlTree(simpleInfo["url"])

        info = {
            "title": firstDefault( element.xpath("//span[contains(@class, 'title_border2')]/text()"), "None" ).strip(),
            "url": simpleInfo["url"],
            "teacher": firstDefault( element.xpath("//th[@class='danger' and text()='授課教師']/following::td/text()"), "None" ).strip(),
            "category": element.base_url,
            "description": "".join( element.xpath("//div[@class='gap']/following::p/text()") ).strip(),
        }

        info["units"] = []
        if not ( urls:= element.xpath("//a[text()='課程影音']/@href") ):
            return info

        videoPageUrl = urljoin(simpleInfo["url"], urls[0])
        element = self._getHtmlTree(videoPageUrl)

        for tr in element.xpath("//table[contains(@class, 'table-bordered')]/tr")[1:]:
            url = urljoin(tr.base_url, firstDefault( tr.xpath(".//a[text()='線上觀看']/@href"), "" ))
            element2 = self._getHtmlTree(url)
            unitInfo = \
            {
                "title": firstDefault( tr.xpath(".//td[2]/text()"), "None" ).strip(),
                "videoUrl": element2.xpath("//iframe/@src")[0]
            }
            info["units"].append(unitInfo)

        return info
