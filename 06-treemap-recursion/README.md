# Avian Biodiversity Treemaps using Recursion

- `treemap.py`: Contains my code for the treemaps.

- `tree.py`: Python file that provides a Tree class.

- `drawing.py`: Python file that provides a function for visualizing a list of rectangles.

- `test_treemap.py`: Python file with automated tests.

- `get_files.sh`: A script for downloading the data. Running it will add two new directories: `data/` and `test_data/`
  - data:
    - birds.json: JSON file containing trees of bird sighting data.
    - sparrows.json: JSON file containing trees in which all of the root's 
      children are leaves.
  - test_data: directory containing files for running the automated tests
    - expected_birds_rectangles.json
    - expected_birds_values_paths.json
    - expected_sparrows_rectangles.json

- `pytest.ini`: A configuration file that you can safely ignore.