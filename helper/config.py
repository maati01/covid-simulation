import argparse

PATH_TO_BIG_POPULATION_ARRAY = "data/big_population_array.npy"
PATH_TO_SMALL_POPULATION_ARRAY = "data/small_population_array.npy"

PATH_TO_BIG_BINARY_ARRAY = "data/big_binary_array.npy"
PATH_TO_SMALL_BINARY_ARRAY = "data/small_binary_array.npy"


def set_mode():
    parser = argparse.ArgumentParser("Simulation settings")
    parser.add_argument("-s", "--size", help="If you want to reduce the number of points on the map, enter '-m small'")
    args = parser.parse_args()

    if args.size == "small":
        return 4, PATH_TO_SMALL_BINARY_ARRAY, PATH_TO_SMALL_POPULATION_ARRAY
    return 1, PATH_TO_BIG_BINARY_ARRAY, PATH_TO_BIG_POPULATION_ARRAY