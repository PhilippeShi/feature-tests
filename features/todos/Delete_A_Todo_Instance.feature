Feature: Delete a todo instance

As a user of the “rest api todo list manager”
I want to delete a todo instance
So that the “rest api todo list manager” can delete the todo instance from the already existing list of todo instances

Background:
    Given the following todo instances exist in the database
        | title          | doneStatus | description |
        | scan paperwork | false      | q           |
        | file paperwork | false      | q           |
        | file paperwork | false      | q           |


Scenario Outline: Delete a todo instance successfully (Normal Flow)
    When the user makes a request to delete a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” deletes the todo instance from the database

    Examples:
        | title          | doneStatus | description |
        | file paperwork | false      | q           |

Scenario Outline: Delete a todo instance unsuccessfully (Error Flow)
    When the user makes a request to delete a todo instance identified by id "<id>" with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then an error "<error>" is returned

    Examples:
        | id | title | doneStatus | description | error                                    |
        | 5  | ss    | a          | a           | Could not find an instance with todos/5 |

    Scenario Outline: Delete a duplicate todo instance (Alternate Flow)
    When the user makes a request to delete a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” deletes the todo instance from the database

    Examples:
        | title          | doneStatus | description |
        | scan paperwork | false      | q           |
        | file paperwork | false      | q           |

