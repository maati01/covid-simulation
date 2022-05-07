import numpy as np
from PIL import Image
import json

MAX_POPULATION = 4000
MAX_VALUE_IN_ARRAY = 255
PATH_TO_JSON = "data/value_to_population.json"
PATH_TO_POPULATION_ARRAY = "data/population_array"
PATH_TO_BINARY_ARRAY = "data/binary_array"


def convert_img_to_population_map(path: str) -> np.array:
    """
    Convert image to population map and save to file.
    """

    img = Image.open(path)
    img = img.convert("L")
    img = np.array(img)

    np.save(PATH_TO_BINARY_ARRAY, img)

    row_size, column_size = img.shape

    value_to_population = {val: int(((MAX_VALUE_IN_ARRAY - val) / MAX_VALUE_IN_ARRAY) * MAX_POPULATION) for val in
                           range(0, 256)}

    for row in range(0, row_size):
        for column in range(0, column_size):
            img[row, column] = value_to_population[img[row, column]]

    with open(PATH_TO_JSON, "w") as outfile:
        json.dump(value_to_population, outfile)
    np.save(PATH_TO_POPULATION_ARRAY, img)
