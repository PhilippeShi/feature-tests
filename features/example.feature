Feature: showing off behave
  As a behave user
  I want to have a simple feature file
  So that I can show off behave

  Scenario: run a simple test
    Given we have behave installed
    When we implement a test
    Then behave will test it for us!

  Scenario: Setup table
    Given the database is filled with the following books
    | Book                  | Author         | Year |
    | The Hobbit            | J.R.R. Tolkien | 1937 |
    | The Lord of the Rings | J.R.R. Tolkien | 1954 |
    | The Silmarillion      | J.R.R. Tolkien | 1977 |
    Then we can read the data table

  