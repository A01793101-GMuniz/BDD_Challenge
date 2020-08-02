from behave import *
from selenium import webdriver

from Features.Common.Utils.Assert import TestAssert
from Features.environment import select_driver_from_config, open_web_page
from Pages.LightningWebComponents.Datatable import Datatable
from Pages.Menus.NavigationMenu import NavigationMenu
from Pages.Menus.SideBarMenu import SideBarMenu
from Pages.Tools.Lightning.Playground import Playground


@given('I launch any browser')
def get_driver(context):
    context.driver = use_fixture(select_driver_from_config, context)


@when('I open salesforce developers application')
def open_salesforce(context):
    use_fixture(open_web_page,context, "https://developer.salesforce.com/docs/component-library/documentation/en/48.0"
                                       "/lwc")


@when('Navigate to Component Reference Tab')
def navigate_to_reference_tab(context):
    NavigationMenu(context.driver).click_comp_ref_menu()


@when('Search in Quick Find for "{value}"')
def quick_find_search(context, value):
    SideBarMenu(context.driver).quick_search_menu = value


@when('I Navigate to a Components>lightning>"{value}" on the left menu panel')
def navigate_to_component(context, value):
    SideBarMenu(context.driver).click_lighting_component(value)


@when('Under Example tab on the main pane I select "{value}" from the dropdown')
def select_example_value(context, value):
    Datatable(context.driver).choose_example_dropdown_value(value)


@when('I Click on the Open in Playground button')
def click_playground_button(context):
    Datatable(context.driver).click_playground_button()


@when('On Preview section I edit row "{id_value}" with the following data "{label}" "{website}" "{phone}" "{'
      'close_at}" "{balance}"')
def edit_all_row_records(context, id_value, label, website, phone, close_at, balance):
    id_to_edit = int(id_value.split(":")[1]) - 1
    context.old_row_data = ({"id": id_to_edit})
    context.actual_new_data = ({"id": id_to_edit})
    context.new_row_data = {"id": id_to_edit,
                            "Label": label,
                            "Website": website,
                            "Phone": phone,
                            "CloseAt": close_at,
                            "Balance": balance
                            }
    row_data = Playground(context.driver).edit_row(context.new_row_data)
    context.old_row_data.update(row_data[0])
    context.actual_new_data.update(row_data[1])


@then('I must validate the changes I have done in the table are present')
def assert_data(context):
    test_assert = TestAssert()
    # Assert Data in Datatable is the one user sent
    test_assert.test_assert_entered_row_data\
        (context.new_row_data, context.actual_new_data,
         f"Data sent from test to modify row id {context.new_row_data['id'] + 1} "
                                                  f"is not on Datatable or it's incomplete")
    test_assert.test_assert_row_data_has_changed\
        (context.actual_new_data, context.old_row_data,
         f"Wrong or incomplete data change on row {context.new_row_data['id'] + 1}")
    context.driver.close()
