from .catcherBase import firstDefault, SinglePageCatcher
from urllib.parse import urljoin
import lxml.etree

class NthuCatcher(SinglePageCatcher):

    URL = "https://ocw.nthu.edu.tw/ocw/index.php?page=courseList&classid=0&order=time&maximum=5000"
    XPATH = {
        "coursesDiv": "//div[contains(@class, 'singleCourse')]",
    }


    def _parsePage(self, page):
        """
        解析 page
        output: dict

        key: "courses",
        """
        info = {"courses": []}
        for div in page.xpath(self.XPATH["coursesDiv"]):
            info["courses"].append(
                {
                    "title": firstDefault( div.xpath(".//span[@class='courseTitle']/text()") ).strip(),
                    "cid": int(
                        firstDefault( div.xpath("./@onclick"), "" )
                        .replace("""window.open('index.php?page=course&cid=""", "")
                        .replace("&');", "")),
                    "category": firstDefault( div.xpath(".//span[@class='courseCategory']/text()"), "None" ).strip(),
                    "teacher": firstDefault( div.xpath(".//span[@class='courseTeacher']/text()"), "None" ).strip(),
                    "imgsrc": urljoin(div.base_url, firstDefault( div.xpath(".//img/@src"), "" )),
                    "description": firstDefault( div.xpath(".//div[@class='courseDescription']//span/text()"), []).strip(),
                })

        return info


    def _catchCourseInfo(self, simpleInfo: dict) -> dict:

        url = f"https://ocw.nthu.edu.tw/ocw/index.php?page=course&cid={simpleInfo['cid']}&"
        element = self._getHtmlTree(url)

        info = {
            "title": simpleInfo["title"],
            "url": url,
            "teacher": simpleInfo["teacher"],
            "category": simpleInfo["category"],
            "description": simpleInfo["description"],
            "imgsrc": simpleInfo["imgsrc"],
        }

        info["units"] = []
        for a in element.xpath("//div[@id='collapse1']//a"):

            unitInfo = \
            {
                "title": firstDefault( a.xpath("./text()"), "None" ).strip(),
                "url": urljoin(a.base_url, firstDefault( a.xpath("./@href"), "" )),
            }

            element2 = self._getHtmlTree(unitInfo["url"])
            if element2.xpath("//img"):
                unitInfo["videoUrls"] = element2.xpath("//img[@title='離線觀看']/../@href") + element2.xpath("//iframe[@name='videoFrame']/@src")
            else:
                unitInfo["videoUrls"] = []

            info["units"].append(unitInfo)

        return info
