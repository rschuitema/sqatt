Feature: Automated issue types configuration for Jira
  In order to quickly and consistently setup a Jira environment
  As a project manager
  I want to have the issue type for Jira configured automatically

  Scenario Outline: Agile issue types
    Given the issue types have been configured
    Then I can create an issue of type <issue type> that have avatar <avatar>

    Examples: issue types
    |issue type     | avatar      |
    |Epic           | lightning   |
    |User Story     | ribbon      |
    |Task           | check mark  |
    |Sub-task       | two squares |
    |Spike          | light bulb  |
    |Technical Debt | heartbeat   |
    |Bug            | white dot   |

