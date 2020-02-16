# Jira
This section describes the default configuration of Jira.
The configuration assumes an agile way of working.

## Issue types
The following issue types are defined:
* Epic
* User Story
* Task
* Sub-task
* Spike
* Technical Debt
* Bug

## Workflow
The workflow in Jira is configured according to the following principle.

![workflow](./workflow.png)

Each issue starts in the state "New". From the state "New" a transition
is possible to the state "To_<Activity>". This state indicates that
the issue is ready for the <Activity> to be performed. When the activity
is started the issue transitions to the <Activity> state. In this state
the actual <Activity> is performed. When the <Activity> is finished the
issue transitions to the "<Activity_Done>" state. There it can be decided
if the issue needs another <Activity> or can transition to the state "Done".

The <Activity> is where projects can extend the workflow. There are a
few default activities defined:
* Analyzing
* Solving
* Reviewing
* Verifying
* Refining

Furthermore an issue can transition to the following states from any
other state:
* Blocked
* Dismissed

This configuration is suitable for different work flows in a project.
E.g. when a team need to refine an issue it can simply take all the issues
in the state "To_refining". When the issues are refined te issue will
transition to the state "To_solving", which means that it can be implemented
in one of the next sprints.

In a similar way it helps the CCB to select the issues that need to be
discussed.

A project can extend the workflow with new activities as long as it
complies with the pattern <To_Activity> -> <Activity> -> <Activity_Done>

## Roles
The following roles are configured in Jira:
* Administrators
* Developer
* Scrum master
* Product owner
* Project manager


## Permission schemes
Jira has several permission schemes
The following sections describe the configuration of each of the
permission schemes.

### Project permissions
This is the scheme for project permission.

| Permission | Description | Role |
| --- |--- |---| 
| Administer projects     | Ability to administer a project in Jira | Administrators |
| Browse projects         | Ability to browse projects and the issues within them | Developers, Viewers |
| Edit sprints            | Ability to edit sprint name and goal | ??? |
| Manage sprints          | Ability to manage sprints | Administrators |
| Start/Complete sprints  | Ability to start and complete sprints | ??? |
| View development tools  | Allows users in a software project to view development-related information on the issue, such as commits, reviews and build information | Developers, Viewers |
| View read only workflow | Users with this permission may view a read-only version of a workflow | Developers, Viewers | 

### Issue permissions


