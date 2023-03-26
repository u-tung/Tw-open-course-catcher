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
