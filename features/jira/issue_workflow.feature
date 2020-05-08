Feature: Automated workflow configuration for Jira
  In order to quickly setup a standardized workflow for a Jira environment
  As a project manager
  I want to have the workflow for Jira configured automatically

  Scenario Outline: Issue states
    Given the workflow has been configured for Jira
    Then an issues can have the state <issue state>

    Examples: workflow status
    | issue state    |
    | New            |
    | To_Analyzing   |
    | To_Solving     |
    | To_Verifying   |
    | To_Refining    |
    | Analyzing      |
    | Solving        |
    | Verifying      |
    | Refining       |
    | Analyzing_Done |
    | Solving_Done   |
    | Verifying_Done |
    | Refining_Done  |
    | Done           |
    | Blocked        |


  Scenario Outline: Developer issue transitions
    Given Jira contains an issue
    Then a developer can transition the issue from <current state> to <new state>
    And from any state except from "Done" to state "Blocked"
    And from the state "Blocked" to its previous state

    Examples: transitions
    | current state  | new state      |
    | New            | To_Analyzing   |
    | New            | To_Solving     |
    | New            | To_Verifying   |
    | New            | To_Refining    |
    | To_Analyzing   | Analyzing      |
    | To_Solving     | Solving        |
    | To_Verifying   | Verifying      |
    | To_Refining    | Refining       |
    | Analyzing      | Analyzing_Done |
    | Solving        | Solving_Done   |
    | Verifying      | Verifying_Done |
    | Refining       | Refining_Done  |
    | Analyzing_Done | Done           |
    | Solving_Done   | Done           |
    | Verifying_Done | Done           |
    | Refining_Done  | Done           |
    | Analyzing_Done | To_Analyzing   |
    | Analyzing_Done | To_Solving     |
    | Analyzing_Done | To_Verifying   |
    | Solving_Done   | To_Analyzing   |
    | Solving_Done   | To_Solving     |
    | Solving_Done   | To_Verifying   |
    | Refining_Done  | To_Refining    |
    | Refining_Done  | To_Solving     |

  Scenario: workflow changes
    Given a Jira workflow is configured
    Then only an administrator can add new issue states and transitions

  Scenario: add issue state and transition
    Given Jira contains an issue
    When an administrator adds a new state "State2"
    And adds a transition from existing state "State1" to "State2"
    Then the issue can transition from "State1" to "State2"
