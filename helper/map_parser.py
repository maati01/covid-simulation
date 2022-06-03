from PIL import Image
import numpy as np
import json

MAX_POPULATION = 4000
MAX_VALUE_IN_ARRAY = 255
PATH_TO_JSON = "data/value_to_population.json"

PATH_TO_BIG_POPULATION_ARRAY = "data/big_population_array.npy"
PATH_TO_SMALL_POPULATION_ARRAY = "data/small_population_array.npy"

PATH_TO_BIG_BINARY_ARRAY = "data/big_binary_array.npy"
PATH_TO_SMALL_BINARY_ARRAY = "data/small_binary_array.npy"

PATH_TO_MAP = "data/map.png"
SCALE = 4


def resize_and_save_array(scale: int) -> None:
    """Converts the array to a smaller size and save to file."""
    binary_array = np.load(PATH_TO_BIG_BINARY_ARRAY)
    population_array = np.load(PATH_TO_BIG_POPULATION_ARRAY)

    row_size, column_size = binary_array.shape

    new_row_size, new_column_size = row_size // scale, column_size // scale

    small_binary_array = binary_array.reshape(
        [new_row_size, row_size // new_row_size, new_column_size, column_size // new_column_size]).mean(3).mean(1)
    small_binary_array = small_binary_array.astype(np.int32)

    np.save(PATH_TO_SMALL_BINARY_ARRAY, small_binary_array)

    small_population_array = population_array.reshape(
        [new_row_size, row_size // new_row_size, new_column_size, column_size // new_column_size]).mean(3).mean(1)
    small_population_array = small_population_array.astype(np.int32)*(SCALE**2)

    np.save(PATH_TO_SMALL_POPULATION_ARRAY, small_population_array)


def convert_img_to_population_map(path: str, value_to_population: dict[tuple[int, int]: int]) -> None:
    """Converts image to population map and save to file."""

    img = Image.open(path)
    img = img.convert("L")
    img = np.array(img)

    np.save(PATH_TO_BIG_BINARY_ARRAY, img)

    row_size, column_size = img.shape
    for row in range(row_size):
        for column in range(column_size):
            img[row, column] = value_to_population[img[row, column]]

    np.save(PATH_TO_BIG_POPULATION_ARRAY, img)


if __name__ == "__main__":
    value_to_population = {val: int(((MAX_VALUE_IN_ARRAY - val) / MAX_VALUE_IN_ARRAY) * MAX_POPULATION) for val in
                           range(0, 256)}

    convert_img_to_population_map(PATH_TO_MAP, value_to_population)
    resize_and_save_array(SCALE)

    with open(PATH_TO_JSON, "w") as outfile:
        json.dump(value_to_population, outfile)
