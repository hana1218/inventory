Feature: The inventory service back-end
    As a Inventory Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | id    | name     | quantity| restock_level | restock_count|condition| first_entry_date | last_restock_date |
        | 12    | computer | 12      | 5             | 2            | NEW     | 2019-11-18       |  2019-12-18       |
        | 321   | phone    | 32      | 2             | 11           | OPEN_BOX| 2020-08-13       |  2020-08-15       |
        | 712   | table    | 43      | 7             | 3            | USED    | 2021-04-01       |  2021-04-05       |
        | 322   | pen      | 12      | 12            | 1            | USED    | 2018-06-04       |  2018-12-02       |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory RESTful Service" in the title
    And I should not see "404 Not Found"

// todo: 
Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Happy"
    And I set the "Category" to "Hippo"
    And I select "False" in the "Available" dropdown
    And I select "Male" in the "Gender" dropdown
    And I set the "Birthday" to "06-16-2022"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Happy" in the "Name" field
    And I should see "Hippo" in the "Category" field
    And I should see "False" in the "Available" dropdown
    And I should see "Male" in the "Gender" dropdown
    And I should see "2022-06-16" in the "Birthday" field

Scenario: List all Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fido" in the results
    And I should see "kitty" in the results
    And I should not see "leo" in the results

Scenario: Search for dogs
    When I visit the "Home Page"
    And I set the "Category" to "dog"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fido" in the results
    And I should not see "kitty" in the results
    And I should not see "leo" in the results

Scenario: Search for available
    When I visit the "Home Page"
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fido" in the results
    And I should see "kitty" in the results
    And I should see "sammy" in the results
    And I should not see "leo" in the results

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "fido"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fido" in the "Name" field
    And I should see "dog" in the "Category" field
    When I change "Name" to "Loki"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Loki" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Loki" in the results
    And I should not see "fido" in the results

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "kitty"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "kitty" in the "Name" field
    And I should see "cat" in the "Category" field
    When I press the "Delete" button
    Then I should see the message "Pet has been Deleted!"