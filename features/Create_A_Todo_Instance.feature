Feature: Create a new todo instance

As a user of the “rest api todo list manager”
I would like to be able to create a new todo instance
So that the “rest api todo list manager” can add the new todo instance to the already existing list of todo instances

Background:
    Given the following todo instances exist in the database:
        | id    | title    	        | doneStatus 	| description    |
        | 1     | scan paperwork	| false         |                |
        | 2  	| file paperwork 	| false         |                |

Scenario Outline: Create a new todo instance successfully (Normal Flow)
    When the user makes a request to create a new todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” assigns a new id "<id>" to the new todo instance and adds it to the database

    Examples:
    | id    | title    	        | doneStatus 	| description           |
    | 1     | scan paperwork	| false         |                       |
    | 2  	| file paperwork 	| false         |                       |
    | 3  	| sign paperwork 	| true          | signature required    |


Scenario Outline: Create a new todo instance unsuccessfully (Error Flow)
    When the user makes a request to create a new todo instance with fields id "<id>", doneStatus "<doneStatus>", description "<description>"
    and nonexistent field title "<title>"
    Then the “rest api todo list manager” returns an error message "<error>"

    Examples:
    | id    | title    	        | doneStatus 	| description           |   error                         |
    | 1     | scan paperwork	| false         |                       |                                 |
    | 2  	| file paperwork 	| false         |                       |                                 |
    | 3  	|                	| true          | signature required    |   "title : field is mandatory"  |

Scenario Outline: Create a duplicate todo instance (Alternate Flow)
    When the user makes a request to create a duplicate todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” assigns a new id "<id>" to the duplicate todo instance and adds it to the database

    Examples:
    | id    | title    	        | doneStatus 	| description           |
    | 1     | scan paperwork	| false         |                       |
    | 2  	| file paperwork 	| false         |                       |
    | 3  	| file paperwork 	| false         |                       |
