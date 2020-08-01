Feature: Inline edit a data table

    Background: Common steps
    Given I launch any browser
    When I open salesforce developers application
    And Navigate to Component Reference Tab
    And Search in Quick Find for "datatable"
    And I Navigate to a Components>lightning>"datatable" on the left menu panel
    And Under Example tab on the main pane I select "Data Table with Inline Edit" from the dropdown


    Scenario: Edit All fields of a row on the database

    And I Click on the Open in Playground button
    And On Preview section I edit row "id:3" with the following data "Larry Page" "https://google.com" "(555)-755-6575" "Jan 1, 2022-12:57 PM" "770.54"
    Then I must validate the changes I have done in the table are present
