# Coding Standards & Guidelines

1. Use the *present tense* for [commit messages](https://www.simplethread.com/git-commit-message-101/). More guidance [here](https://chris.beams.io/git-commit#seven-rules)
1. Write human and machine readable commit messages - https://www.conventionalcommits.org/en/v1.0.0/
1. Commit messages feed into the PR description
1. PR descriptions feed into the RELEASE NOTES
1. For a PR, `git rebase` is used to clean up and fold multiple commits
1. Keep commits small and targeted - no big commits with 100+ files all being changed in different ways
1. Keep commit messages brief but meaningful and relevant
1. The PEP-8 standards are fully adopted
1. We use [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) date format `YYYY-MM-DD` and `YYYY-MM-DDTHH:mm:ss` for datetime
1 All timestamps are always in UTC
1. Make your code self-documenting
1 Use meaningful, readable function names and variable names
