# Workshop Management System

A full-stack application for managing workshops with lifecycle states, participant signups, and challenge visibility control.

## Project Structure

```
workshop-management-system/
├── backend/                 # TypeScript/Node.js API
│   ├── src/
│   │   ├── controllers/    # HTTP request handlers
│   │   ├── services/       # Business logic
│   │   ├── database/       # JSON database files
│   │   └── types/          # TypeScript interfaces
│   ├── package.json
│   ├── tsconfig.json
│   └── jest.config.js
│
└── frontend/               # Next.js application
    ├── pages/             # Next.js pages
    ├── components/        # React components
    ├── lib/              # Utilities and API client
    ├── package.json
    ├── tsconfig.json
    └── tailwind.config.js
```

## Technology Stack

### Backend
- TypeScript
- Node.js
- Express
- JSON database
- Jest + fast-check for testing

### Frontend
- Next.js
- React
- TailwindCSS
- Jest + React Testing Library

## Quick Start

### Backend Setup
```bash
cd backend
npm install
npm run dev
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Features

- Workshop lifecycle management (pending → ongoing → completed)
- Participant signup control based on workshop status
- Challenge visibility control
- RESTful API with JSON persistence
- Property-based testing for correctness guarantees

## Testing

Both backend and frontend include:
- Unit tests for specific scenarios
- Property-based tests for universal correctness
- Coverage thresholds (80% lines, 75% branches)

Run tests:
```bash
# Backend
cd backend && npm test

# Frontend
cd frontend && npm test
```

## Documentation

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [Requirements Document](./.kiro/specs/workshop-management-system/requirements.md)
- [Design Document](./.kiro/specs/workshop-management-system/design.md)
