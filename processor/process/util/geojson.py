import ast
from typing import Dict

from prefect import task


@task
def as_geojson(raw_string: str) -> Dict:
    """ reads geojson """
    return ast.literal_eval(raw_string)
