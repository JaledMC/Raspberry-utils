import json


def remove_class(region):
    if region["region_attributes"]["class"] == 1:
        return True
    if region["region_attributes"]["class"] == 2:
        return True
    if region["region_attributes"]["class"] == 3:
        return True
    if region["region_attributes"]["class"] == 4:
        return False


with open("/home/gangstar0v0t/Desktop/maderas_garcia_varona/datasets/1.json") as file:
    dataset = json.load(file)

for name, image in dataset.items():
    image["regions"] = [region for region in image["regions"] if remove_class(region)]


with open("/home/gangstar0v0t/Desktop/maderas_garcia_varona/datasets/cleaned.json", 'w') as out_file:
    json.dump(dataset, out_file)
