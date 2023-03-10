Feature: Change a project title

  As a user
  I want to change the title of a project instance
  So that I can view projects with new titles

  Background:
    Given the application is running
    And the following project exist
      | title       | completed | active | description |
      | Office Work | false     | false  |             |

  Scenario Outline: Change project title only (Normal flow)
    Given a project with "<old_title>" exists
    When I update the project with "<new_title>"
    Then the project is updated
    And the response returns status "<code>"
    Examples:
      | old_title   | new_title  | code |
      | Office Work | Im quit    | 200  |
      | Game Work   | Keep going | 200  |

  Scenario Outline: Change project title and description (Alternate flow)
    Given a project with "<old_title>" and "<old_description>" exist
    When I update the project with "<new_title>" and "<new_description>" together
    Then the project is updated
    And the response returns status "<code>"
    Examples:
      | old_title | old_description | new_title | new_description | code |
      | oldT1     | oldD1           | newT1     | newD1           | 200  |
      | oldT2     | oldD2           | newT2     | newD2           | 200  |

  Scenario Outline: Change project title that not exist (Error flow)
    Given a project with "<id>" not exist
    When I update the project with "<title>"
    Then the response returns status "<code>"
    And an error "<message>" is returned
    Examples:
      | id   | title | code | message                      |
      | 2455 | newT  | 404  | Invalid GUID for 2455 entity project|