# Workshop Management System - Frontend

Frontend application for the Workshop Management System built with Next.js and TailwindCSS.

## Project Structure

```
frontend/
├── pages/              # Next.js pages
├── components/         # React components
├── lib/               # Utility functions and API client
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── jest.config.js
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

4. Run tests:
```bash
npm test
```

## Features

- Workshop listing display
- Status-based styling
- Signup availability indicators
- Error handling and loading states
- Responsive design with TailwindCSS

## Environment Variables

Create a `.env.local` file:
```
NEXT_PUBLIC_API_URL=http://localhost:3001
```
