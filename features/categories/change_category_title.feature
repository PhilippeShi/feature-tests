Feature: Edit a category title
    As a user
    I want to edit a category title
    So that I can view the category with the new title

    Background:
        Given the application is running
        And the following categories exist
        | title  | description |
        | Home   |             |
        | Office |             |
        | Travel | Flights     |
        | Other  | Notes       |

    Scenario Outline: Change category title only (Normal flow)
        Given a category with "<old_title>" exists
        When I update the category with "<new_title>"
        Then the category is updated
        And the response returns status "<code>"
        Examples:
        | old_title | new_title | code |
        | Travel    | Holiday   | 200  |
        | Other     | Misc      | 200  |

    Scenario Outline: Change category title with same description (Alternate flow)
        Given a category with "<old_title>" and "<old_description>" exists
        When I update the category with both "<new_title>" and "<new_description>"
        Then the category is updated
        And the response returns status "<code>"
        Examples:
        | old_title | new_title | old_description | new_description | code |
        | Travel    | Holiday   | Flights         | Flights         | 200  |
        | Other     | Misc      | Notes           | Notes           | 200  |

    Scenario Outline: Change category that does not exist (Error flow)
        Given a category with "<id>" does not exist
        When I get the category by id
        Then the response returns status "<code>"
        And an error "<message>" is returned
        Examples:
        | id | message | code |
        | 3  | Could not find an instance with categories/3 | 404 |
        | 4  | Could not find an instance with categories/4 | 404 |
    
