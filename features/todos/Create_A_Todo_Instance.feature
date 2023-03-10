Feature: Create a new todo instance

  As a user of the “rest api todo list manager”
  I want to create a new todo instance
  So that the “rest api todo list manager” can add the new todo instance to the already existing list of todo instances

  Background:
    Given the following todo instances exist in the database

      | title          | doneStatus | description |
      | scan paperwork | false      | 1           |
      | file paperwork | false      | 2           |

  Scenario Outline: Create a new todo instance successfully (Normal Flow)
    When the user makes a request to create a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” adds the todo instance to the database

    Examples:
      | title          | doneStatus | description        |
      | sign paperwork | true       | signature required |


  Scenario Outline: Create a new todo instance unsuccessfully (Error Flow)
    When the user makes a request to create a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then an error "<error>" is returned
    And the todo instance is not created


    Examples:
      | title | doneStatus | description        | error                      |
      | null  | true       | signature required | title : field is mandatory |

  Scenario Outline: Create a duplicate todo instance (Alternate Flow)
    When the user makes a request to create a todo instance with fields title "<title>", doneStatus "<doneStatus>", and description "<description>"
    Then the “rest api todo list manager” adds the todo instance to the database

    Examples:
      | title          | doneStatus | description |
      | file paperwork | false      | null        |

