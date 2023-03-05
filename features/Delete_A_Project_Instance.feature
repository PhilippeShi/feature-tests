Feature: Delete a project instance

As a user of the “rest api todo list manager”
I want to delete a project instance
So that the “rest api todo list manager” can delete the project instance from the already existing list of project instances

Background:
    Given the following project instances exist in the database:
        | id    | title    	        | completed 	| active    |   description     |
        | 1     | Office Work   	| false         | false     |                   |
        | 2     | Office Work       | false         | true      |                   |


Scenario Outline: Delete a project instance successfully (Normal Flow)
    When the user makes a request to delete a project instance identified by id "<id>" with fields title "<title>",
    completed status "<completed>", active status "<active>" and description "<description>"
    Then the “rest api todo list manager” deletes the project instance from the database

    Examples:
    | id    | title    	        | completed 	| active    |   description     |
    | 2     | Office Work       | false         | true      |                   |

Scenario Outline: Delete a project instance unsuccessfully (Error Flow)
    When the user makes a request to delete a project instance identified by id "<id>" with fields title "<title>",
    completed status "<completed>", active status "<active>" and description "<description>" that does not exist in the database
    Then the “rest api todo list manager” returns an error message "<error>"

    Examples:
    | id    | title    	        | completed 	| active    |   description     |  error                                       |
    | 1     | Office Work   	| false         | false     |                   |                                              |
    | 2     | Office Work       | false         | true      |                   |                                              |
    | 5  	|                   |               |           |                   |  Could not find any instances with projects/ |

Scenario Outline: Delete a duplicate project instance (Alternate Flow)
    When the user makes a request to delete a duplicate project instance identified by id "<id>" with fields title "<title>",
    completed status "<completed>", active status "<active>" and description "<description>"
    Then the “rest api todo list manager” deletes the duplicate project instance identified by id "<id>"

    Examples:
    | id    | title    	        | completed 	| active    |   description     |
    | 1     | Office Work   	| false         | false     |                   |

