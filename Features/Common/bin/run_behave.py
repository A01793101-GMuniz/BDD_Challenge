import os

import behave
from behave.__main__ import main as behave_main

if __name__ == '__main__':
    feature_path = os.path.dirname(os.path.dirname(__file__)).replace("/Common", "")
    behave_main(f"{feature_path}/InlineEditADataTable.feature -D browser=Firefox")
