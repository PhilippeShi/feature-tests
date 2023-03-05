Feature: Get a todo instance

As a user of the “rest api todo list manager”
I want to get a todo instance
So that the “rest api todo list manager” can display a todo instance from the database

Background:
    Given the following todo instances exist in the database:
        | id    | title    	        | doneStatus 	| description    |
        | 1     | scan paperwork	| false         |                |
        | 2  	| file paperwork 	| false         |                |
        | 3  	| file paperwork 	| false         |                |

Scenario Outline: Get a todo instance successfully (Normal Flow)
    When the user makes a request to get a todo instance identified by id "<id>" with fields title "<title>",
    doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” returns a todo instance from the database

    Examples:
    | id    | title    	        | doneStatus 	| description    |
    | 1     | scan paperwork	| false         |                |

Scenario Outline: Get a todo instance unsuccessfully (Error Flow)
    When the user makes a request to get a todo instance identified by id "<id>" with fields
    doneStatus "<doneStatus>", description "<description>" and title "<title>" that does not exist in the database
    Then the “rest api todo list manager” returns an error message "<error>"

    Examples:
    | id    | title    	        | doneStatus 	| description           |   error                                     |
    | 1     | scan paperwork	| false         |                       |                                             |
    | 2  	| file paperwork 	| false         |                       |                                             |
    | 3  	|                	|               |                       |   Could not find an instance with todos/    |

Scenario Outline: Get a duplicate todo instance (Alternate Flow)
    When the user makes a request to get a duplicate todo instance identified by id "<id>" with fields title "<title>",
    doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” returns the first duplicate todo instance identified by id "<id>" from the database

    Examples:
    | id    | title    	        | doneStatus 	| description           |
    | 1     | scan paperwork	| false         |                       |
    | 2  	| file paperwork 	| false         |                       |
    | 3  	| file paperwork 	| false         |                       |
