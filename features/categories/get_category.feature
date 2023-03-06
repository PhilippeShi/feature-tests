Feature: Get category
    As a user
    I want to get a category
    So that I can see the information about the category

    Background:
        Given the application is running
        And the following categories exist
        | id | title  | description |
        | 1  | Home   |             |
        | 2  | Office |             |

    Scenario Outline: Get category (Normal flow)
        Given a category with "<id>" exists
        When I get the category by id
        Then the response returns the category object
        And the response returns status "<code>"
        Examples:
        | id | code |
        | 1  | 200  |
        | 2  | 200  |

    Scenario Outline: Get category by title (Alternate flow)
        Given a category with "<title>" exists
        When I get the category by title
        Then the response returns the category object
        And the response returns status "<code>"
        Examples:
        | title | code |
        | Home  | 200  |
        | Office| 200  |

    Scenario Outline: Get category that does not exist (Error flow)
        Given a category with "<id>" does not exist
        When I get the category by id
        Then the response returns status "<code>"
        And an error "<message>" is returned
        Examples:
        | id | message | code |
        | 3  | Could not find an instance with categories/3 | 404 |
        | 4  | Could not find an instance with categories/4 | 404 |
    
