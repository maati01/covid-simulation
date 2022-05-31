import argparse
from logic.models import *

PATH_TO_BIG_POPULATION_ARRAY = "data/big_population_array.npy"
PATH_TO_SMALL_POPULATION_ARRAY = "data/small_population_array.npy"

PATH_TO_BIG_BINARY_ARRAY = "data/big_binary_array.npy"
PATH_TO_SMALL_BINARY_ARRAY = "data/small_binary_array.npy"

PATH_TO_EXTENDED_COLOR_BAR = "data/extended_color_bar.jpg"
PATH_TO_COLOR_BAR = "data/color_bar.jpg"


def model(s: str):
    s = s.upper()
    models = {'SEIR': SEIR, 'SEIQR': SEIQR}
    if s not in models:
        raise argparse.ArgumentTypeError(f"Model `{s}` is not supported. Available ones {models}")

    return models[s]


def set_mode():
    parser = argparse.ArgumentParser("Simulation settings")
    parser.add_argument("-s", "--size", help="If you want to reduce the number of points on the map, enter '-s small'")
    parser.add_argument("-m", "--model", type=model, default=SEIR, help="Model to be used in simulation, ex. SEIR")
    args = parser.parse_args()

    if args.size == "small":
        return 4, PATH_TO_SMALL_BINARY_ARRAY, PATH_TO_SMALL_POPULATION_ARRAY, PATH_TO_EXTENDED_COLOR_BAR, args.model
    return 1, PATH_TO_BIG_BINARY_ARRAY, PATH_TO_BIG_POPULATION_ARRAY, PATH_TO_COLOR_BAR, args.model
