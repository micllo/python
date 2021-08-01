import xml.etree.cElementTree as ET


et = ET.ElementTree(file="./file/xml_demo.xml")

for ele in et.findall(".//用例集合/*"):
    if ele.attrib["run"] == "1":
        print(ele.tag)
        print(type(ele))
