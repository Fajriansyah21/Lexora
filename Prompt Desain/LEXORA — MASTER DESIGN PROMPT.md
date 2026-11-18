# LEXORA — MASTER DESIGN PROMPT

Design a complete responsive SaaS web application named **Lexora**, an Indonesian-first AI writing workspace with two core products:

1. AI Text Detector
2. AI Humanizer

The application should feel like a professional writing and analysis workspace, not a generic AI startup landing page.

## 1. Visual Direction

Design concept: **Calm Editorial Intelligence**.

The visual identity should communicate:
- Clarity
- Trust
- Precision
- User control
- Professional writing experience

Use an editorial, spacious, minimal, and calm interface.

Avoid:
- Purple-to-blue gradients
- Glassmorphism
- Excessive rounded cards
- Unnecessary decorative illustrations
- Fake analytics and vanity metrics
- Excessive shadows
- Generic AI-generated dashboard aesthetics

## 2. Design System

### Color Palette

- Primary: #0F766E
- Primary Dark: #134E4A
- Primary Light: #DDF3EF
- Background: #F7F8F7
- Surface: #FFFFFF
- Secondary Surface: #EEF2F0
- Primary Text: #17231F
- Secondary Text: #66736E
- Border: #DCE5E1
- Success: #15803D
- Warning: #B45309
- Danger: #B42318
- Information: #2563EB
- Mixed Result: #6D5BD0

Do not communicate important states through color alone. Always include text labels or icons.

### Typography

- Headings: Plus Jakarta Sans, weight 600–700.
- Body and UI: Inter, weight 400–600.
- Technical metadata and counters: JetBrains Mono.

Use 16px as the standard body text size. Maintain comfortable line height and strong readability.

### Layout

- Desktop application sidebar: 240px.
- Admin sidebar: 256px.
- Top navigation: 64px.
- Application content maximum width: 1440px.
- Public content maximum width: 1280px.
- Base spacing unit: 4px.
- Panel radius: 14px.
- Input and button radius: 10px.
- Minimum button and touch target height: 44px.

## 3. Shared Application Shell

All authenticated user pages must share a consistent application shell.

Desktop:
- Fixed left sidebar.
- Top navigation with Lexora identity, credit balance, notifications, and account avatar.
- Main content area.
- Consistent page heading and supporting description.

Sidebar navigation:
- Overview
- AI Text Detector
- AI Humanizer
- Style Profiles
- History
- Credits & Transactions
- Support
- Privacy Center
- Settings

Mobile:
- Compact top navigation.
- Bottom navigation for Home, Detector, Humanizer, and Account.
- Secondary pages accessible through Account or More.
- Do not simply compress the desktop sidebar.

## 4. Product Behavior Requirements

### AI Text Detector

The Detector must use four possible result labels:

- HUMAN
- AI
- MIXED
- UNCERTAIN

Never display:
- Authorship percentages
- Numeric probability scores
- Fake confidence meters
- Claims that the result proves who wrote the text

Show this disclaimer near the result:

"Hasil ini menunjukkan pola teks, bukan bukti pasti siapa penulisnya."

MIXED and UNCERTAIN must have different visual treatments and explanations.

The Detector input supports:
- Text input
- TXT, DOCX, and PDF upload
- Maximum 20,000 extended grapheme clusters
- Optional language hint
- Credit estimate

There is no hard minimum text length. Short texts may produce UNCERTAIN results.

### AI Humanizer

The Humanizer must provide:
- Original text editor
- Generated result editor
- Built-in writing style selector
- Personal style profile selector
- Character counter
- Credit estimate
- Run action
- Compare changes
- Copy result
- Download
- Save to history

Supported input length: 100–50,000 extended grapheme clusters.

The original text must remain unchanged unless the user edits it.

Show this warning:

"Periksa kembali fakta, angka, kutipan, dan makna sebelum menggunakan hasil."

Do not promise that generated text is undetectable.

## 5. Accessibility

Target WCAG 2.2 AA.

Include:
- Visible keyboard focus
- Readable contrast
- Clear field labels
- Semantic headings
- Keyboard-friendly controls
- Minimum 44px touch targets
- Accessible modal behavior
- Reduced-motion support
- Screen-reader-friendly status messages

## 6. Language and Copywriting

Use concise, natural Indonesian for the primary interface.

Keep the tone professional, clear, and measured.

Avoid exaggerated marketing claims.

Do not invent:
- User statistics
- Testimonials
- Detection accuracy
- Product performance metrics
- Pricing
- Credit package values

Use placeholders for server-configured prices and credit amounts.

## 7. Design Consistency

Create reusable components and maintain consistent:
- Color tokens
- Typography
- Spacing
- Button variants
- Form controls
- Navigation
- Cards
- Status labels
- Modal dialogs
- Empty states
- Loading states

Generate desktop and mobile variants.

Use this master prompt as the visual foundation for every subsequent Lexora screen. Do not change the established design system between screens.