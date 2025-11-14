# Frontend

React-based frontend application for NotAgenticB2BSaaS using MaterialUI.

## Tech Stack

- **React** - JavaScript UI library
- **Material-UI (MUI)** - Component library
- **Vite** - Build tool and dev server

## Features

- Global theme configuration using MaterialUI Theme Context
- Responsive component structure:
  - NavBar - Navigation header
  - Main - Main content area with feature cards
  - Footer - Footer with links and information

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The application will start on `http://localhost:3000`

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── NavBar.jsx
│   │   ├── Main.jsx
│   │   └── Footer.jsx
│   ├── theme/
│   │   └── theme.js
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── vite.config.js
└── package.json
```

## Customization

### Theme

The global theme can be customized in `src/theme/theme.js`. You can modify:
- Color palette
- Typography
- Component styles
- Spacing and breakpoints
