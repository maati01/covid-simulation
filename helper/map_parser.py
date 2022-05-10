import numpy as np
from PIL import Image
import json

MAX_POPULATION = 4000
MAX_VALUE_IN_ARRAY = 255
PATH_TO_JSON = "data/value_to_population.json"

PATH_TO_BIG_POPULATION_ARRAY = "data/big_population_array"
PATH_TO_MID_POPULATION_ARRAY = "data/mid_population_array"
PATH_TO_SMALL_POPULATION_ARRAY = "data/small_population_array"

PATH_TO_BIG_BINARY_ARRAY = "data/big_binary_array"
PATH_TO_MID_BINARY_ARRAY = "data/mid_binary_array"
PATH_TO_SMALL_BINARY_ARRAY = "data/small_binary_array"


#TODO poprawic to zapisywanie XD

def resize_and_save_json(array: np.array, x_size: int, y_size: int, value_to_population: dict[tuple[int, int]: int]):
    mid_x_size, mid_y_size = x_size//4, y_size//4
    small_x_size, small_y_size = x_size//16, y_size//16


    mid_array = array.reshape([mid_x_size, x_size // mid_x_size, mid_y_size, y_size // mid_y_size]).mean(3).mean(1)
    small_array = array.reshape([small_x_size, x_size // small_x_size, small_y_size, y_size // small_y_size]).mean(3).mean(1)
    mid_array = mid_array.astype(np.int32)
    # np.save(PATH_TO_BIG_BINARY_ARRAY, array)
    np.save(PATH_TO_MID_BINARY_ARRAY, mid_array)
    # np.save(PATH_TO_SMALL_BINARY_ARRAY, array)

    print(array.sum())
    print(mid_array.sum()*16)
    for i in range(mid_x_size):
        for j in range(mid_y_size):
            mid_array[i, j] = value_to_population[int(mid_array[i, j])]

    print(mid_array.sum())

def convert_img_to_population_map(path: str) -> np.array:
    """
    Convert image to population map and save to file.
    """

    img = Image.open(path)
    img = img.convert("L")
    img = np.array(img)

    row_size, column_size = img.shape
    mid_x_size, mid_y_size = row_size // 4, column_size // 4

    value_to_population = {val: int(((MAX_VALUE_IN_ARRAY - val) / MAX_VALUE_IN_ARRAY) * MAX_POPULATION) for val in
                           range(0, 256)}

    resize_and_save_json(img, row_size,column_size, value_to_population)


    for row in range(0, row_size):
        for column in range(0, column_size):
            img[row, column] = value_to_population[img[row, column]]

    print(img.sum())
    mid_array = img.reshape([mid_x_size, row_size // mid_x_size, mid_y_size, column_size // mid_y_size]).mean(3).mean(1)
    mid_array = mid_array.astype(np.int32)
    print(mid_array.sum()*16)
    with open(PATH_TO_JSON, "w") as outfile:
        json.dump(value_to_population, outfile)
    np.save(PATH_TO_MID_POPULATION_ARRAY, mid_array)

if __name__ == "__main__":
    convert_img_to_population_map("data/map.png")