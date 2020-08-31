import os
from datetime import datetime

from allure_behave.hooks import allure_report
from behave.__main__ import main as behave_main

from Features.Common.Utils.MainScreen import MainScreen

if __name__ == '__main__':
    feature_path = os.path.dirname(os.path.dirname(__file__)).replace("/Features/Common", "")
    main_screen = MainScreen(feature_path)
    report_path = "behave_run_" + datetime.now().strftime("%d%m%Y_%X").replace(":", "")

    # behave_main(f"{main_screen.feature_path}/{main_screen.feature_to_run} ")
    # -D browsers_label={main_screen.browser_to_run} ")
    behave_main(f"{main_screen.feature_path}/{main_screen.feature_to_run} -D browser={main_screen.browser_to_run} "
                f"--tags @first "
                f"-f allure_behave.formatter:AllureFormatter -o {feature_path}/Reports/results/{report_path}")

    # allure_report(f"{feature_path}/Reports/results/{report_path}")

