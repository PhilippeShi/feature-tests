Feature: Change a todo title

  As a user
  I want to change the title of a todo instance
  So that I can view todos with new titles

  Background:
    Given the following todos exist
      | title          | doneStatus | description |
      | scan paperwork | false      |             |
      | file paperwork | false      |             |

  Scenario Outline: Change todo title only (Normal flow)
    Given a todo with "<old_title>" exists
    When I update the todo with "<new_title>"
    Then the todo is updated
    And the response returns status "<code>"
    Examples:
      | old_title   | new_title  | code |
      | School      | SChool work| 200  |
      | Game Work   | Keep going | 200  |

  Scenario Outline: Change todo title and description (Alternate flow)
    Given a todo with "<old_title>" and "<old_description>" exist
    When I update the todo with "<new_title>" and "<new_description>" together
    Then the todo is updated
    And the response returns status "<code>"
    Examples:
      | old_title  | old_description | new_title  | new_description | code |
      | old title  | old description | new title  | new description | 200  |
      | old title2 | old desc        | new title2 | new desc        | 200  |

  Scenario Outline: Change todo title that not exist (Error flow)
    Given a todo with "<id>" not exist
    When I update the todo with "<title>"
    Then the response returns status "<code>"
    And an error "<message>" is returned
    Examples:
      | id   | title | code | message                             |
      | 2455 | newT  | 404  | Invalid GUID for 2455 entity todo   |