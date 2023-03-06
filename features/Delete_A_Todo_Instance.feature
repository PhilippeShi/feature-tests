Feature: Delete a todo instance

As a user of the “rest api todo list manager”
I want to delete a todo instance
So that the “rest api todo list manager” can delete the todo instance from the already existing list of todo instances

Background:
    Given the following todo instances exist in the database:
        | id    | title    	        | doneStatus 	| description    |
        | 1     | scan paperwork	| false         |                |
        | 2  	| file paperwork 	| false         |                |
        | 3  	| file paperwork 	| false         |                |


Scenario Outline: Delete a todo instance successfully (Normal Flow)
    When the user makes a request to delete a todo instance with fields title "<title>", doneStatus "<doneStatus>",
    and description "<description>"
    Then the “rest api todo list manager” deletes the todo instance from the database

    Examples:
    | id    | title    	        | doneStatus 	| description           |
    | 2  	| file paperwork 	| false         |                       |
    | 3  	| file paperwork 	| false         |                       |

Scenario Outline: Delete a todo instance unsuccessfully (Error Flow)
    When the user makes a request to delete a todo instance with fields title "<title>", doneStatus "<doneStatus>",
    and description "<description>"
    Then the “rest api todo list manager” returns an error message "<error>"

    Examples:
    | id    | title    	        | doneStatus 	| description           |   error                                      |
    | 5  	|                   |               |                       |   Could not find any instances with todos/   |

Scenario Outline: Delete a duplicate todo instance (Alternate Flow)
    When the user makes a request to delete a todo instance with fields title "<title>", doneStatus "<doneStatus>",
    and description "<description>"
    Then the “rest api todo list manager” deletes the todo instance from the database

    Examples:
    | id    | title    	        | doneStatus 	| description           |
    | 1     | scan paperwork	| false         |                       |
    | 3  	| file paperwork 	| false         |                       |

