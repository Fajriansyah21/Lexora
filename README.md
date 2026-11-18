# Lexora

Platform untuk membantu pengguna menganalisis dan mengolah tulisan melalui **AI Text Detector** dan **AI Humanizer**.

## Setup development (Windows 10/11)

### Prasyarat

- Git for Windows.
- Node.js 26 LTS atau lebih baru.
- Corepack aktif, atau pnpm 9.15.0 dipasang sesuai dokumentasi resmi pnpm.
- Python 3.12 atau 3.13 dan `pip` untuk pengujian Python.

### Instalasi

Buka PowerShell atau Windows Terminal pada root repo:

```powershell
corepack enable
corepack prepare pnpm@9.15.0 --activate
pnpm install
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-test.txt pytest
```

### Pemeriksaan lokal

```powershell
pnpm lint
pnpm format:check
pnpm test
python -m pytest
```

`pnpm format` menulis formatting; `pnpm format:check` hanya memeriksa.

## Workspace layout

- `apps/web`: workspace placeholder untuk aplikasi web; belum ada business logic.
- `packages/config`: workspace kecil untuk memverifikasi pnpm/Turborepo dan test TypeScript.
- `tests`: Python test foundation; test dataset yang sudah ada tetap berada di tempatnya.

## Batas Stage 7

Tahap M1 menyediakan tooling, struktur workspace, test harness, CI dasar, dan panduan setup. Belum ada database schema, authentication, API bisnis, domain logic, pilihan model AI, atau aktivasi payment provider. Jangan memulai M2 sebelum M1 direview dan disetujui project owner.

## Dokumentasi

- [User flows](plan/USER-FLOWS.md)
- [System design](plan/SYSTEM-DESIGN.md)
- [Security architecture and threat model](plan/SECURITY-ARCHITECTURE-AND-THREAT-MODEL.md)
- [Data flow and lifecycle](plan/DATA-FLOW-AND-DATA-LIFECYCLE.md)
- [API contracts](plan/API-CONTRACTS.md)
- [Technology evaluation](plan/TECHNOLOGY-EVALUATION.md)
- [UI/UX specification](plan/UI-UX-SPECIFICATION.md)
- [Design Freeze Review](docs/DESIGN-FREEZE-REVIEW-2026-11-18.md)
- [Visual design exports](Desain/)
- [Google Stitch design prompts](plan/STITCH-DESIGN-PROMPTS.md)
- [Antigravity skill setup](docs/ANTIGRAVITY-SKILL-SETUP.md)

- [Acceptance criteria baseline](plan/ACCEPTANCE-CRITERIA.md)
- [Critical acceptance test scenarios](plan/ACCEPTANCE-TEST-SCENARIOS.md)

Mulai dari [indeks dokumentasi proyek](plan/README.md).

Dokumen utama:
- [Product Overview](plan/PRODUCT-OVERVIEW.md)
- [Requirements Elicitation Status](plan/REQUIREMENTS-ELICITATION-STATUS.md)
- [System Requirements Analysis](plan/SYSTEM-REQUIREMENTS-ANALYSIS.md)
- [Decision Log](plan/DECISION-LOG.md)
- [Active Roadmap](plan/ACTIVE-ROADMAP.md)

## Aturan kerja

Baca [AGENTS.md](AGENTS.md) sebelum melakukan pekerjaan di repository. Requirement, keputusan, rencana, hasil pengujian, dan status implementasi harus dibedakan serta diverifikasi.

## Cakupan MVP

MVP berfokus pada AI Text Detector dan AI Humanizer. DOCX Metadata Cleaner ditunda ke fase setelah MVP. Lihat Product Overview dan Decision Log untuk batas cakupan yang disahkan.

## Riset dataset

- [Privacy and legal readiness checklist](docs/PRIVACY-AND-LEGAL-READINESS.md)

- [Supporting modules requirements audit](docs/SUPPORTING-MODULES-REQUIREMENTS-AUDIT-2026-11-17.md)

- [AI Text Detector requirements audit](docs/AI-TEXT-DETECTOR-REQUIREMENTS-AUDIT-2026-11-17.md)

- [Humanizer requirements audit](docs/HUMANIZER-REQUIREMENTS-AUDIT-2026-11-17.md)

- [Dataset specification and benchmark protocol](docs/DATASET-SPECIFICATION-BENCHMARK-v1.md)
- [Annotation guidelines](docs/ANNOTATION-GUIDELINES-v1.md)
- [Dataset JSON Schema](schemas/dataset-records-v1.schema.json)
- [Editing history template](templates/editing-history.template.json)
- [Editing history export mapping](docs/EDITING-HISTORY-MAPPING-v1.md)
- [Synthetic dataset test harness](tests/synthetic_dataset/README.md)
- [Latest synthetic test report](results/synthetic-dataset-test-2026-11-17.md)
