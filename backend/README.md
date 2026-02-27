# Workshop Management System - Backend

Backend API for the Workshop Management System built with TypeScript, Node.js, and Express.

## Project Structure

```
backend/
├── src/
│   ├── controllers/     # HTTP request handlers
│   ├── services/        # Business logic
│   ├── database/        # JSON database files and operations
│   ├── types/          # TypeScript interfaces
│   └── index.ts        # Application entry point
├── package.json
├── tsconfig.json
└── jest.config.js
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Build the project:
```bash
npm run build
```

3. Run in development mode:
```bash
npm run dev
```

4. Run tests:
```bash
npm test
```

## Database

The backend uses JSON files for data persistence:
- `workshops.json` - Workshop records
- `participants.json` - Participant records
- `challenges.json` - Challenge records

## API Endpoints

- `GET /api/workshops` - List all workshops
- `POST /api/workshops` - Create new workshop
- `PATCH /api/workshops/:id/status` - Update workshop status
- `PATCH /api/workshops/:id/signup-flag` - Toggle signup flag
- `POST /api/workshops/:id/signup` - Register participant
- `GET /api/workshops/:id/participants` - List participants
- `POST /api/workshops/:id/challenges` - Create challenge
- `GET /api/workshops/:id/challenges` - List challenges (with access control)
- `GET /api/challenges/:id` - Get challenge details (with access control)
