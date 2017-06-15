# coding: utf-8

import wiki
import pandas as pd

nations = pd.read_csv("../data/nations.csv")
for name in nations["name"]:
    text = wiki.get_text(name)
    if text is None:
        continue
    print(name)
