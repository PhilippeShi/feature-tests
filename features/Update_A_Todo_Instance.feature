Feature: Update a todo instance

As a user of the “rest api todo list manager”
I want to update a todo instance
So that the “rest api todo list manager” can update the todo instance from the already existing list of todo instances

Background:
    Given the following todo instances exist in the database:
        | id    | title    	        | doneStatus 	| description    |
        | 1     | scan paperwork	| false         |                |
        | 2  	| file paperwork 	| false         |                |
        | 3  	| file paperwork 	| false         |                |


Scenario Outline: Update a todo instance successfully (Normal Flow)
    When the user makes a request to update a todo instance titled "<title>" with fields title "<newTitle>",
    doneStatus "<newDoneStatus>", and description "<newDescription>"
    Then the “rest api todo list manager” updates the todo instance from the database

    Examples:
    | title    	        | newTitle        | doneStatus 	|   newDoneStatus  |  description  |   newDescription     |
    | scan paperwork	| sign paperwork  | false       |   true           |               |   not signed yet     |


Scenario Outline: Update a todo instance unsuccessfully (Error Flow)
    When the user makes a request to update a todo instance identified by id "<id>" with fields title "<title>", doneStatus "<doneStatus>",
    and description "<description>"
    Then the “rest api todo list manager” returns an error message "<error>"

    Examples:
    | id    | title    	        | doneStatus 	| description           |   error                                                  |
    | 8  	| send paperwork    | false         | send to government    |   No such todo entity instance with GUID or ID 8 found   |

Scenario Outline: Update a duplicate todo instance (Alternate Flow)
    When the user makes a request to update a todo instance titled "<title>" with fields title "<newTitle>",
    doneStatus "<newDoneStatus>", and description "<newDescription>"
    Then the “rest api todo list manager” updates the todo instance from the database

    Examples:
    | title    	        | newTitle        | doneStatus 	|   newDoneStatus  |  description  |   newDescription     |
    | file paperwork	| do paperwork    | false       |   false          |               |   not done yet       |




e