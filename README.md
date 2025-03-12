# Awesome Design Docs

A collection of design docs

- [English](https://github.com/charliesbot/design-docs/tree/main/english)
- [Spanish](https://github.com/charliesbot/design-docs/tree/main/spanish)


Design Doc Structure
A design doc should discuss the following aspects:

Use-Cases: The interactions between a user and a system to attain particular goals.

Acceptance Criteria: Conditions that must be satisfied to consider the feature as done.

Background: Stuff one needs to know to understand the use-cases (e.g. motivating examples, previous versions and problems, links to related changes/design docs, etc.)

Possible Solutions: Possible solutions with the pros and cons, and explanation of implementation details.

Conclusion: Which decision was made and what were the reasons for it.

As community we want to collaborate on design docs as much as possible and write them together, in an iterative manner. To make this work well design docs are split into multiple files that can be written and refined by several persons in parallel:

index.md: Entry file that links to the files below (also see 'dev-design-doc-index-template.md').

use-cases.md: Describes the use-cases, acceptance criteria and background (also see 'dev-design-doc-use-cases-template.md').

solution-<n>.md: Each possible solution (with the pros and cons, and implementation details) is described in a separate file (also see 'dev-design-doc-solution-template.md').

conclusion.md: Describes the conclusion of the design discussion (also see 'dev-design-doc-conclusion-template.md').

It is expected that:

An agreement on the use-cases is achieved before solutions are being discussed in detail.

Anyone who has ideas for an alternative solution uploads a change with a solution-<n>.md that describes their solution. In case of doubt whether an idea is a refinement of an existing solution or an alternative solution, it’s up to the owner of the discussed solution to decide if the solution should be updated, or if the proposer should start a new alternative solution.

All possible solutions are fairly discussed with their pros and cons, and treated equally until a conclusion is made.

Unrelated issues (judged by the design doc owner) that are identified during discussions may be extracted into new design docs (initially consisting only of an index.md and a use-cases.md file). Doing so is optional yet can be done by either the design owner or reviewers.

Changes making iterative improvements can be submitted frequently (e.g. additional uses-cases can be added later, solutions can be submitted without describing implementation details, etc.).

After a conclusion has been approved contributors are expected to keep the design doc updated and fill in gaps while they go forward with the implementation.

https://gerrit-review.googlesource.com/Documentation/dev-design-docs.html#structure