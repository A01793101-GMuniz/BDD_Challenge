import os

import behave
from behave.__main__ import main as behave_main

from Features.environment import InitialConfig

if __name__ == '__main__':
    feature_path = os.path.dirname(os.path.dirname(__file__)).replace("/Features/Common", "")
    features_to_run = "InlineEditADataTable.feature"
    browser_to_run = "Firefox"

    config = InitialConfig(feature_path,features_to_run, browser_to_run)
    behave_main(f"{config.feature_path}/Features/{config.features_to_run} -D browser={config.browser_to_run}  -f "
                f"allure_behave.formatter:AllureFormatter -o {feature_path}/Reports/results")
