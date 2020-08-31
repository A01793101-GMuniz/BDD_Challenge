Feature: Inline edit a data table

    Background: Common steps
        Given I launch any browser
        When I open salesforce developers application
        And Navigate to Component Reference Tab
        And Search in Quick Find for "datatable"
        And I Navigate to a Components>lightning>"datatable" on the left menu panel
        And Under Example tab on the main pane I select "Data Table with Inline Edit" from the dropdown
        And I Click on the Open in Playground button


    @first
    Scenario: Edit All fields of a row on the database
        When On Preview section I edit row "id:3" with the following data "Larry Page" "https://google.com" "(555)-755-6575" "Jan 1, 2022-12:57 PM" "770.54"
        Then I must validate the changes I have done in the table are present


    @slow
    Scenario Outline: Edit specific field of a row on the datatable

        When On Preview section I edit row "<id>" field "<field_to_edit>" with the following data "<data>"
        Then I must validate the changes I have done in the table are present

        Examples:
        |  id   |   field_to_edit |             data            |
        | id:70 |   Website       |   https://www.facebook.com  |
        | id:99 |   Label         |   Guillermo Muniz           |
        | id:50 |   Phone         |   51-1-3321818282           |

