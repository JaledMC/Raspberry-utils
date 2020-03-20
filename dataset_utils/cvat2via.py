import xml.etree.ElementTree as ET
import argparse
import json


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_option(
        "-f", "--file",
        help="xml annotation file",
        )
    parser.add_option(
        "-o", "--output_file",
        help="converted via json file",
    )
    return parser.parse_args()


class Annotation:
    """
    class to convert cvat xml annotations to via json annotations
    args:
        xml cvat file, with annotations made with "polyline" and "polygon"
    return:
        save a json file in via format
    """
    def __init__(self, image_id, name, width, height, regions):
        self.image_id = image_id
        self.name = name
        self.width = width
        self.height = height
        self.regions = regions
        self.size = width*height

    @classmethod
    def from_xml(cls, image):
        image_id = image.get('id')
        name = image.get('name')
        width = int(image.get('width'))
        height = int(image.get('height'))
        regions = cls.get_regions(image)
        return cls(image_id, name, width, height, regions)

    def get_regions(image):
        """
        Parse cvat polylines and polygons to via regions
        """
        regions = []
        for region in image.findall('polyline')+image.findall('polygon'):
            clase = region.get('label')
            points = region.get('points')
            regions.append(Annotation.via_region(clase, points))
        return regions

    def via_region(clase, points):
        """
        Returns a dict with the region in via format
        """
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
        """
        Change cvat format [x1,y1,x2,y2...] to [x1,x2,x3...][y1,y2,y3...]
        """
        all_points_x = []
        all_points_y = []
        for point in points.split(";"):
            x, y = point.split(",")
            all_points_x.append(round(float(x)))
            all_points_y.append(round(float(y)))
        return all_points_x, all_points_y

    def get_dict(self):
        """
        Returns a dict with the complete image in via format
        """
        return {
            "filename": self.name,
            "dimension": [self.width, self.height],
            "size": self.size,
            "file_attributes:": {},
            "regions": self.regions
        }


def main():
    args = parse_options()
    root = ET.parse(args.file).getroot()
    dataset = {}
    for image in root.findall('image'):
        annotation = Annotation.from_xml(image)
        dataset[annotation.name] = annotation.get_dict()
    with open(args.output_file, 'w') as out_file:
        json.dump(dataset, out_file)


if __name__ == "__main__":
    main()
