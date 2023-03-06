Feature: Get a todo instance

As a user of the “rest api todo list manager”
I want to get a todo instance
So that the “rest api todo list manager” can display a todo instance from the database

Background:
    Given the following todo instances exist in the database
        | id    | title    	        | doneStatus 	| description    |
        | 1     | scan paperwork	| false         | null           |
        | 2  	| file paperwork 	| false         | null           |
        | 3  	| file paperwork 	| false         | null           |

Scenario Outline: Get a todo instance successfully (Normal Flow)
    When the user makes a request to get a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” returns a todo instance from the database

    Examples:
    | title    	        | doneStatus 	| description    |
    | scan paperwork	| false         | null           |

Scenario Outline: Get a todo instance unsuccessfully (Error Flow)
    When the user makes a request to get a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” returns an error message "<error>"

    Examples:
    | id    | title    	        | doneStatus 	| description           |   error                                     |
    | 6  	| null              | null          | null                  |   Could not find an instance with todos/6   |

Scenario Outline: Get a duplicate todo instance (Alternate Flow)
    When the user makes a request to get a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” returns a todo instance from the database

    Examples:
    | title    	        | doneStatus 	| description           |
    | file paperwork 	| false         | null                  |
