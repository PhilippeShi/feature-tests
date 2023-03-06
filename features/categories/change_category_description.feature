Feature: Edit a category description
    As a user
    I want to edit a category description
    So that I can view the category with the new description

    Background:
        Given the application is running
        And the following categories exist
        | title  | description |
        | Home   |             |
        | Office |             |
        | Travel | Flights     |
        | Other  | Notes       |

    Scenario Outline: Change category description only (Normal flow)
        Given a category with description "<old_description>" exists
        When I update the category description with "<new_description>"
        Then the category is updated
        And the response returns status "<code>"
        Examples:
        | old_description | new_description | code |
        | Flights         | Cruises         | 200  |
        | Notes           | Misc            | 200  |

    Scenario Outline: Change category description with same title (Alternate flow)
        Given a category with "<old_title>" and "<old_description>" exists
        When I update the category with both "<new_title>" and "<new_description>"
        Then the category is updated
        And the response returns status "<code>"
        Examples:
        | old_title | new_title | old_description | new_description | code |
        | Travel    | Travel    | Flights         | Cruises         | 200  |
        | Other     | Other     | Notes           | Misc            | 200  |

    Scenario Outline: Change category description with empty title (Error flow)
        Given a category with description "<old_description>" exists
        When I update the category with both "<new_title>" and "<new_description>"
        Then the category is not updated
        And the response returns status "<code>"
        And an error "<message>" is returned
        Examples:
        | old_description | new_description | new_title | code | message                    |
        | Flights         | Cruises         |    null   | 400  | title : field is mandatory |
        | Notes           | Misc            |    null   | 400  | title : field is mandatory |

    
