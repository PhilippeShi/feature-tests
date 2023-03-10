Feature: Change the description of a project
  As a user
  I want to change the title of a project instance
  So that I can view projects with new descriptions

  Background:
    Given the application is running
    And the following project exist
      | title       | completed | active | description |
      | Office Work | false     | false  |             |

  Scenario Outline: Change project description only (Normal flow)
    Given a project with description "<old_description>" exists
    When I update the project with description "<new_description>"
    Then the project is updated
    And the response returns status "<code>"
    Examples:
      | old_description | new_description | code |
      | Office Work     | Im quit         | 200  |
      | Game Work       | Keep going      | 200  |

  Scenario Outline: Change project description with same title (Alternate flow)
    Given a project with "<old_title>" and "<old_description>" exist
    When I update the project with "<new_title>" and "<new_description>" together
    Then the project is updated
    And the response returns status "<code>"
    Examples:
      | old_title | old_description | new_title | new_description | code |
      | oldT1     | oldD1           | oldT1     | newD1           | 200  |
      | oldT2     | oldD2           | oldT2     | newD2           | 200  |

  Scenario Outline: Change project description that not exist (Error flow)
    Given a project with "<id>" not exist
    When I update the project with description "<description>"
    Then the response returns status "<code>"
    And an error "<message>" is returned
    Examples:
      | id   | description | code | message                              |
      | 2455 | newD        | 404  | Invalid GUID for 2455 entity project |