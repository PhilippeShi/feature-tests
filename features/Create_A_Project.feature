# Created by 29752 at 2023/3/5
Feature: Create a new project instance

  As a user of the “rest api todo list manager”
  I want to create a new project instance
  So that I can organize my tasks by category

  Background:
    Given the application is running
    And the following project exist
      | id | title       | completed | active | description |
      | 1  | Office Work | false     | false  |             |


  Scenario Outline: Create a project (Normal flow)
    Given a project with "<title>" and "<completed>" and "<active>" and "<description>"
    When I create the the project
    Then the project is created
    Examples:
      | title       | completed | active | description     |
      | mobile app  | false     | true   | android project |
      | windows app | true      | false  | windows project |
      | macos app   | true      | true   | macos project   |

  Scenario Outline: Create a project with an existing title (Alternate flow)
    Given a project with "<title>" and "<completed>" and "<active>" and "<description>"
    When I create the project
    Then the project is created
    And the new project object is different from the existing project
    Examples:
      | title       | completed | active | description |
      | Office Work |true       |true    |updated      |

  Scenario Outline: Create a project with missing description (Alternate Flow)
    Given a project with "<title>" and "<completed>" and "<active>" and "<description>"
    When I create the project
    Then the project is created
    Examples:
      | title                   | completed | active | description |
      | Project no description1 | false     | false  | null        |
      | Project no description2 | true      | false  | null        |

  Scenario Outline: Create a category with a missing title (Error flow)
    Given a project with "<title>" and "<completed>" and "<active>" and "<description>"
    When I create the project
    Then the project is not created
    And an error "<message>" is returned
    Examples:
      | title | completed | active | description   | message |
      | null  | false     | false  | a description |title :  field is mandatory|
