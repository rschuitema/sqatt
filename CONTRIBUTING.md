# Contributing to SQATT

First off, thanks for taking the time to contribute!

The following is a set of guidelines for contirbuting to SQATT.
These are mostly guidelines, not rules.
Use your best judgment, and feel free to propose changes to this document in a pull request.

## Quality

As this repository is all about measuring the quality of software, we cannot write code that complies to high standards.
Therefore the quality of the SQATT codebase is checked in 3 ways: With github actions, Codacy and with Better Code Hub.
The codebase follows the rules as defined by the python community.
It is checked with tools like pylint, black, pycodestyle, pydocstyle etc.

## Testing

It is highly appreciated and encouraged to write unit tests.
Pull requests that also have unit tests are more likely to be accepted.
The current code base does not have unit tests for all code, but the intention is to gradually add unit tests.

## Reporting Bugs

Before creating bug reports check if it is new one.
Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible.
* **Provide specific examples to demonstrate the steps**.
Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples.
If you're providing snippets in the issue, use
[Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is
the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**

Include details about your configuration and environment:

* **Which version of SQATT are you using**?
* **Which version of pyton are you using**?
* **What's the name and version of the OS you're using**?

## Suggesting Enhancements

Before suggesting an enhancement check if it is a new enhancement.
Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/).

Provide the following information when describing the enhancement suggestion:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**.
Include copy/pasteable snippets which you use in those examples, as
[Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Explain why this enhancement would be useful**.
* **Specify which version of SQATT you are using**.
* **Specify the name and version of the OS you're using**.

## Pull Requests

Keep teh pull requests small.
Follow the quality guidelines of the python community.
After you submit your pull request,
verify that all [status checks](https://help.github.com/articles/about-status-checks/) are passing.

While the prerequisites above must be satisfied prior to having your pull request reviewed,
the reviewer(s) may ask you to complete additional design work, tests,
or other changes before your pull request can be ultimately accepted.
