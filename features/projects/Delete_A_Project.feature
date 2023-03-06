Feature: Delete a project instance

  As a user of the “rest api todo list manager”
  I want to delete a project instance
  So that the “rest api todo list manager” can delete the project instance from the already existing list of project instances

  Background:
    Given the following project exist
      | title       | completed | active | description |
      | Office Work | false     | false  |             |


  Scenario Outline: Delete a project instance successfully (Normal Flow)
    Given a project with "<title>" exists
    When I delete the project
    Then the project is deleted
    And the response returns status "<code>"
    Examples:
      | title       | code |
      | Office Work | 200  |

  Scenario Outline: Delete a project instance with title and description (Alternate flow)
    Given a project with "<title>" and "<description>" exist
    When I delete the project
    Then the project is deleted
    And the response returns status "<code>"
    Examples:
      | title       | description | code |
      | Office Work | des         | 200    |

  Scenario Outline: Delete a project instance unsuccessfully (Error Flow)
    Given a project with "<id>" not exist
    When I delete the project
    Then an error "<messages>" is returned
    And the response returns status "<code>"

    Examples:
      | id   | messages                                        | code |
      | 1145 | Could not find any instances with projects/1145 | 404  |

