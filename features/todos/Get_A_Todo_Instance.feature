Feature: Get a todo instance

As a user of the “rest api todo list manager”
I want to get a todo instance
So that the “rest api todo list manager” can display a todo instance from the database

Background:
    Given the following todo instances exist in the database
        | title          | doneStatus | description |
        | scan paperwork | false      | null        |
        | file paperwork | false      | null        |
        | file paperwork | false      | null        |

Scenario Outline: Get a todo instance successfully (Normal Flow)
    When the user makes a request to get a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” returns a todo instance from the database

    Examples:
    | title    	        | doneStatus 	| description    |
    | scan paperwork	| false         | null           |

Scenario Outline: Get a todo instance unsuccessfully with empty parameters (Error Flow)
    When the user makes a request to get a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the response returns status "<code>"
    And the length of returned list should be "<length>"

    Examples:
        | id | title | doneStatus | description | code | length |
        | 6  | null  | null       | null        | 200  |0       |

    Scenario Outline: Get a duplicate todo instance (Alternate Flow)
    When the user makes a request to get a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” returns a todo instance from the database

    Examples:
    | title    	        | doneStatus 	| description           |
    | file paperwork 	| false         | null                  |
