# covid-simulation

## FIRST RUN
`pip install -r requirements.txt ` \
`python helper/map_parser.py` \
`python helper/color_bar_generator.py`

## RUN APP
`python run.py` \
`python run.py -s small` - version with fewer points in the model \
`python run.py -m SEIQR` - using different model than SEIR (Possibles ones: SEIR, SEIQR, SEIQRD, SEIQRD2, SEIQRD2V)