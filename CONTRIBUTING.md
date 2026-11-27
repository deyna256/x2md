# Contributing to x2md

Use plain English in issues, commits, documentation and code comments. See the [README](README.md) for the public API.

## No signatures

Do not add generated-by lines, tool attribution footers or similar signatures anywhere: not in commits,
pull requests, reviews, comments, issues, documentation or code.

## Issues

Check for an existing issue before opening one. Give each issue one clear outcome and a short title
that describes the problem or intended change.

Report security vulnerabilities privately to a maintainer.

Use the [issue template](.github/ISSUE_TEMPLATE/issue.md) to describe the problem, its impact and how someone can tell it is fixed. For conversion bugs,
include the input format, a small shareable sample and the expected and actual Markdown.

Keep the issue self-contained. Add examples, relevant links and scope limits when useful.
Keep credentials and private document content out of examples and logs.

Give each issue one type label: `bug`, `feature`, `maintenance`, `docs` or `question`. Add `ci` for CI
and developer tooling, and `good first issue` for small, self-contained tasks. Close duplicates and
declined issues with the matching close reason instead of a label.

## Branches

For issue work, branch from `main` and use only the issue number as the branch name. For issue #1:

```sh
git switch main
git switch -c 1
```

Keep the branch focused on its issue. For work without an issue, use a short descriptive name
such as `readme-typo`.

## Commits

Write one line in English, starting with the issue number and an action, for example
`#1: preserve headings when converting DOCX`. For work without an issue, omit the
number, as in `fix a typo in the README`.

Keep each commit focused. Inspect the staged diff. Omit the commit body and [signatures](#no-signatures).

## Checks

Install the development dependencies with `uv sync --locked`. Use the commands in the [Justfile](Justfile):

| command | what it does |
|---|---|
| `just test` | runs the test suite |
| `just lint` | checks formatting, style and import order, changing nothing |
| `just format` | formats the code and applies the fixes ruff can make on its own |
| `just type` | checks types |
| `just build` | builds the wheel and source distribution |
| `just ci` | runs lint, type checks, tests and the build |

Run `just format`, then `just lint`. Fix any remaining issues.

Run the relevant checks before submitting changes. Documentation-only changes need link and formatting
checks, not tests.

The [CI workflow](.github/workflows/ci.yml) runs the tests on Ubuntu with Python 3.12, 3.13 and
3.14. On Python 3.12 it also checks formatting, lint and types, builds the distributions and
checks that the installed wheel includes `py.typed`.

## Tests

Tests live in [tests/](tests/). Test through the public interface. For a conversion regression,
use the smallest shareable input that reproduces it and check the affected Markdown content
or structure.

## Pull requests

Use the [pull request template](.github/pull_request_template.md). Explain the problem, the
change and how you checked it. Include migration steps for breaking changes. Link the issue
with `Closes #<number>` when the PR completes it. Keep the description and docs current as you
revise the code.

Open the pull request as a draft while the work is in progress. When it is ready, mark it ready for review
and request a review from [@deyna256](https://github.com/deyna256) or another maintainer. Do this again after you address
the review's findings, so the reviewer knows the pull request is ready for another look.

## Reviews

Review the change against the issue and the [review checklist](#review-checklist). Explain what
happens, why it matters and how you checked it.

Put every code-anchored finding in an inline comment on the line it concerns and keep the review body
for the verdict and for anything that spans files. Mark a finding that is not blocking with one of
these prefixes:

- **Nit:** small or stylistic; the author may skip it.
- **Question:** you need an answer before you can judge the code.

Everything else blocks the merge until it is resolved.

Use these sections in the review body, and omit a section with nothing in it:

- **Summary:** one sentence on what the change does and whether it is ready.
- **Blocking:** one item per problem, each with `file:line`, the consequence and a concrete fix or check.
- **Non-blocking:** nits, questions and follow-ups worth recording.
- **Checked:** the commands you ran and anything you could not verify.

Request changes only when a finding is blocking. Approve when the rest are nits and say which ones you
expect to be handled. Take work outside the scope of the pull request to a separate issue and link it
instead of growing the review. Do not [sign](#no-signatures) the review or its comments.

### Review checklist

- Explain changes to the public API or the handler contract in the pull request.
- Errors say what failed and where. Keep private document content out of diagnostics.
- New behaviour has a test.
- `just lint`, `just type` and `just test` pass.

## Documentation

Keep shared documentation in Markdown. Distinguish planned behaviour from what the code implements.

| document | covers |
|---|---|
| [README](README.md) | what x2md is and how to start |
| [CONTRIBUTING.md](CONTRIBUTING.md) | how to propose, make and review a change |

Update affected docs and links in the same change. Give each rule one home.

### Local working documents

Use `.local/` at the repository root for research, drafts and development plans; for example,
`.local/research/` and `.local/plans/`. Git ignores this directory. Do not commit it or force-add its
contents.

Move accepted decisions and their essential reasons into shared documentation. Local proposals do not
become requirements without agreement. Shared docs must not require or link to local notes: a fresh
clone must contain everything needed to understand and work on the project.
