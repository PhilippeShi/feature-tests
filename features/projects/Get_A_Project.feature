# Created by 29752 at 2023/3/5
Feature: Get a project instance
  As a user
  I want to get a project
  So that I can see the information about the project

  Background:
    Given the application is running
    And the following project exist
      | id | title       | completed | active | description |
      | 1  | Office Work | false     | false  |             |

  Scenario Outline: Get project (Normal flow)
    Given a project with "<id>" exists
    When I get the project by id
    Then the response returns the project object
    And the response returns status "<code>"
    Examples:
      | id | code |
      | 1  | 200  |

  Scenario Outline: Get project by title (Alternate flow)
    Given a project with "<title>" exists
    When I get the project by title
    Then the response returns the project object
    And the response returns status "<code>"
    Examples:
      | title       | code |
      | Office Work | 200  |

    Scenario Outline: Get project that does not exist (Error flow)
      Given a project with "<id>" does not exist
      When I get the project by id
      Then the response returns status "<code>"
      And an error "<message>" is returned
      Examples:
        | id | code | message                                    |
        | 5  | 404  | Could not find an instance with projects/5 |
        | 6  | 404  | Could not find an instance with projects/6 |


