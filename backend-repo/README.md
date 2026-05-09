# telegram-config-vray-backend

Backend repository for generating subscription outputs and publishing them to:

`hadifarajvand/telegram-config-vray` (`main` branch)

This repo owns:
- scraper and converter code
- generation workflow
- publish/sync logic

The target repo should contain only generated output artifacts.

## Publish Target

- Target repository: `hadifarajvand/telegram-config-vray`
- Target branch: `main`
- Synced content: output directories and output README only

## Required Secret

Set this repository secret in GitHub:

- `OUTPUT_REPO_PAT`: Personal Access Token with `contents:write` on `hadifarajvand/telegram-config-vray`

## Workflow

Workflow file:

`/.github/workflows/generate-and-publish.yml`

Schedule:

- every 2 hours
- manual dispatch
