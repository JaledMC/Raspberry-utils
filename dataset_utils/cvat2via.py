import xml.etree.ElementTree as ET
import json


class Annotation:
    def __init__(self, image_id, name, width, height, regions):
        self.image_id = image_id
        self.name = name
        self.width = width
        self.height = height
        self.regions = regions
        self.size = width*height

    @classmethod
    def from_xml(cls, image):
        """
        From cvat xml
        """
        image_id = image.get('id')
        name = image.get('name')
        width = int(image.get('width'))
        height = int(image.get('height'))
        regions = cls.get_regions(image)
        return cls(image_id, name, width, height, regions)

    def get_regions(image):
        regions = []
        for region in image.findall('polyline')+image.findall('polygon'):
            clase = region.get('label')
            points = region.get('points')
            regions.append(Annotation.via_region(clase, points))
        return regions

    def via_region(clase, points):
        all_points_x, all_points_y = Annotation.points_format(points)
        return {
            "region_attributes": {
                "class": clase
            },
            "shape_attributes": {
                "all_points_x": all_points_x,
                "all_points_y": all_points_y,
                "name": "polygon"
            },
        }

    def points_format(points):
        all_points_x = []
        all_points_y = []
        for point in points.split(";"):
            x, y = point.split(",")
            all_points_x.append(round(float(x)))
            all_points_y.append(round(float(y)))
        return all_points_x, all_points_y

    def get_dict(self):
        return {
            "filename": self.name,
            "dimension": [self.width, self.height],
            "size": self.size,
            "file_attributes:": {},
            "regions": self.regions
        }


if __name__ == "__main__":
    path = "/home/gangstar0v0t/Downloads/BSH_dataset/final.xml"
    root = ET.parse(path).getroot()
    dataset = {}
    for image in root.findall('image'):
        annotation = Annotation.from_xml(image)
        dataset[annotation.name+str(annotation.size)] = annotation.get_dict()
    with open("via.json", 'w') as out_file:
        json.dump(dataset, out_file)
