Feature: Update a todo instance

As a user of the “rest api todo list manager”
I want to update a todo instance
So that the “rest api todo list manager” can update the todo instance from the already existing list of todo instances

Background:
    Given the following todo instances exist in the database
        | title          | doneStatus | description |
        | email paperwork | false      | null        |
        | write paperwork | false      | null        |
        | write paperwork | false      | null        |


Scenario Outline: Update a todo instance successfully (Normal Flow)

    When the user makes a request to update a todo instance titled "<title>" with fields title "<newTitle>", doneStatus "<newDoneStatus>", and description "<newDescription>"
    Then the “rest api todo list manager” updates the todo instance from the database

    Examples:
    | title    	        | newTitle        | doneStatus 	|   newDoneStatus  |  description  |   newDescription     |
    | email paperwork	| sign paperwork  | false       |   true           |  null         |   not signed yet     |
    | write paperwork   | send paperwork  | false       |   true           |  finished     |   sent to government |


Scenario Outline: Update a todo instance unsuccessfully (Error Flow)
    When the user makes a request to update a todo instance identified by id "<id>" with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then an error "<error>" is returned
    And the todo is not updated

    Examples:
    | id    | title    	        | doneStatus 	| description           |   error                                     |
    | 8  	| email paperwork   | false         | send to government    |   Could not find an instance with todos/8   |
    | -1  	| email paperwork   | false         | send to government    |   Could not find an instance with todos/-1   |

Scenario Outline: Update a duplicate todo instance (Alternate Flow)
    When the user makes a request to update a todo instance titled "<title>" with fields title "<newTitle>", doneStatus "<newDoneStatus>", and description "<newDescription>"
    Then the “rest api todo list manager” updates the todo instance from the database

    Examples:
    | title    	        | newTitle        | doneStatus 	|   newDoneStatus  |  description  |   newDescription     |
    | write paperwork	| do paperwork    | false       |   false          |  null         |   not done yet       |


