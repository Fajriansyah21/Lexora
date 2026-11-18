# LEXORA — STYLE PROFILES

Create a Style Profiles management page.

### Main Page

Display:
- Page title: "Style Profiles"
- Description explaining personal writing profiles.
- Create Profile button.

Each profile card displays:
- Profile name.
- Main profile indicator.
- Profile status.
- Number of eligible samples.
- Manage action.

### Create Profile Flow

Create a step-based interface:

1. Enter profile name.
2. Add sample text or upload a supported document.
3. Validate sample length.
4. Review sample collection.
5. Run profile quality evaluation.

Each sample must contain at least 500 extended grapheme clusters.

At least three eligible samples are required before profile evaluation can begin.

Three samples do not guarantee activation. Adaptive quality evaluation may request additional samples.

### Limits

- Maximum six profiles per account.
- Maximum twenty samples per profile.

### Sample Management

Show:
- Active samples.
- Recently Deleted samples.
- Restore action for eligible deleted samples.
- Permanent deletion confirmation.

Recently Deleted applies to samples, not permanently deleted profiles.

Create clear empty states and progress indicators.