from .catcherBase import DoublePageCatcherBase, firstDefault
import lxml.etree

class NtuCatcher(DoublePageCatcherBase):

    URL = "http://ocw.aca.ntu.edu.tw/ntu-ocw/ocw/coupage/1"
    XPATH = {
        "nextUrl": "//a[@title='下一頁']/@href",
        "courseDiv": "//div[contains(@class, 'coursebox')]",
    }


    def _parsePage(self, page):
        """
        解析 page
        output: dict

        key: "courses",
        """
        pageinfo = {}
        pageinfo["courses"] = []

        for div in page.xpath(self.XPATH["courseDiv"]):
            pageinfo["courses"].append({
                "imgsrc": firstDefault( div.xpath(".//img/@src"), "None" ),
                "title": firstDefault( div.xpath(".//div[@class='coursetitle']/a/text()"), "None" ).strip(),
                "url": firstDefault( div.xpath(".//a/@href"), "None" ).strip(),
                "teacher": firstDefault( div.xpath(".//div[@class='teacher']/text()"), "None" ).strip(),
                "introtext": firstDefault( div.xpath(".//div[@class='introtext']/text()"), "None" ).strip(),
            })

        return pageinfo


    def _catchCourseInfo(self, simpleInfo: dict) -> dict:
        element = self._getHtmlTree(simpleInfo["url"])

        info = {
            "title": firstDefault( element.xpath("//h2[@class='title']/text()"), "None" ).strip(),
            "url": simpleInfo["url"],
            "teacher": simpleInfo["teacher"],
            "introtext": firstDefault( element.xpath("//div[@id='course_description']/p/text()"), "None" ).strip(),
            "imgsrc": firstDefault( element.xpath("//div[@id='course_pic']/img/@src"), "None" ),
            "count": firstDefault( element.xpath("//div[@id='count']/text()"), "None" ).strip(),
            "unit": firstDefault( element.xpath("//h4[@class='unit']/text()"), "None" ).strip(),
            "unitNumber": int(firstDefault( element.xpath("//span[@class='number']/text()"), 0 )),
        }

        info["units"] = []
        for i, div in enumerate( element.xpath("//div[@class='AccordionPanel']") ):
            url = "/".join(info["url"].split("/")[:7]) + f"/{i+1}"
            element2 = self._getHtmlTree(url)
            info["units"].append({
                "title": firstDefault( div.xpath(".//div[@class='AccordionPanelTab-text']/text()[2]"), "None" ).strip(),
                "videoUrl": firstDefault( element2.xpath("//iframe/@src") )
            })

        return info
