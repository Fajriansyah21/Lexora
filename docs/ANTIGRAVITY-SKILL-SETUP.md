# Antigravity Skills Setup for Lexora

- **Tanggal:** 2026-11-17
- **Purpose:** prepare the local Antigravity workspace for the later UI implementation phase.
- **Important:** this remote repository session cannot install software into the user's local Windows/Antigravity installation. The commands below are prepared for execution from the local Lexora repository root.

## 1. Recommended skills

### UI UX Pro Max — install now for design work

Use this for design-system generation, style exploration, color/typography selection, and layout recommendations.

PowerShell:
```powershell
npm install -g ui-ux-pro-max-cli
Set-Location F:\Relopoli\Website-AI-Ditector
uipro init --ai antigravity
```

The CLI is the current installation path documented by the project. Do not use the older `uipro-cli` package.

### Impeccable — install before frontend implementation

Use this for UX critique, accessibility/responsive audits, polish, and edge-case hardening once components exist.

PowerShell:
```powershell
Set-Location F:\Relopoli\Website-AI-Ditector
npx impeccable install
```

The current installer documents Google Antigravity support and installs its project skill/hooks. Review generated files before committing them.

### Task Observer — recommended for multi-step project work

Use this to capture reusable workflow observations and maintain the project observation log. The upstream skill is licensed CC BY 4.0; retain attribution when copying/adapting its contents.

Upstream source: https://github.com/iamneilroberts/claude-skills/tree/main/skills/task-observer

### Stop Slop — optional for copy/document review

Use for editing public-facing copy and long documentation, not as a design system or implementation framework.

Upstream source: https://github.com/hardikpandya/stop-slop

## 2. Not selected for the core Lexora SaaS UI

### Huashu Design
The skill is strongest for product-launch animations, motion design, interactive prototypes, slide decks, and infographics. Those are not required for the current MVP UI/UX scope. Do not add it to the default project workflow unless a launch animation or promotional artifact becomes an explicit deliverable.

## 3. Local verification after installation

1. Confirm Antigravity detects the installed skills.
2. Confirm the UI UX Pro Max skill directory and required reference/data files exist.
3. Run the skill's design-system workflow against the Lexora brief.
4. Compare its output with the approved [UI/UX Specification](../plan/UI-UX-SPECIFICATION.md); the project specification remains authoritative.
5. Before committing generated skill files, inspect the diff and ensure no secrets, machine-specific paths, or generated cache files are included.
6. Run Impeccable critique/audit only after a local UI implementation exists.

## 4. Source references

- UI UX Pro Max: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Impeccable: https://github.com/pbakaus/impeccable
- Huashu Design: https://github.com/pc-software-org/huashu-design-en
- Stop Slop: https://github.com/hardikpandya/stop-slop
- Vercel Skills CLI and Antigravity agent support: https://github.com/vercel-labs/skills
- Task Observer: https://github.com/iamneilroberts/claude-skills/tree/main/skills/task-observer

## 5. Installation status

- UI UX Pro Max: **Not installed locally by this remote session**; command prepared.
- Impeccable: **Not installed locally by this remote session**; command prepared.
- Task Observer: source reviewed; project observation log maintained in repository.
- Stop Slop: source reviewed; guidance applied to project copy/document review.
- Huashu Design: reviewed and intentionally not selected for the core SaaS UI.
