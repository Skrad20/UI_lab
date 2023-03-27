from dataclasses import dataclass
from code_app import models as m
import pandas as pd


@dataclass
class DataForContext:
    numbers_sample_from_invertory: list
    numbers_sample_from_profil: list
    date: str
    model_mutter: m.BaseModelAnimal
    model_descendant: m.BaseModelAnimal
    list_number_faters: list
    dataset_faters: pd.DataFrame
    flag_mutter: bool
