# Workshop Management System - Frontend

Next.js frontend application for the Workshop Management System.

## Setup

```bash
# Install dependencies
npm install
```

## Running

```bash
# Development mode (with hot reload)
npm run dev

# Production build
npm run build
npm start
```

The frontend will be available at `http://localhost:3000`

## Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

## Features

- Workshop listing with real-time updates
- Status badges (pending, ongoing, completed)
- Signup availability indicators
- Responsive design with TailwindCSS
- Error handling and loading states
- API integration with retry logic

## Project Structure

```
frontend/
├── pages/
│   └── index.tsx        # Main page
├── components/
│   ├── WorkshopCard.tsx      # Individual workshop display
│   ├── WorkshopCard.test.tsx
│   ├── WorkshopList.tsx      # Workshop list container
│   └── WorkshopList.test.tsx
├── lib/
│   └── api.ts           # API client with error handling
├── styles/
│   └── globals.css      # Global styles
├── public/              # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

## API Configuration

The frontend connects to the backend API at `http://localhost:3535/api`

This is configured in `next.config.js` as a proxy to avoid CORS issues during development.

## Environment Variables

Create a `.env.local` file for custom configuration:

```env
NEXT_PUBLIC_API_URL=http://localhost:3535
```

## Building for Production

```bash
# Build optimized production bundle
npm run build

# Start production server
npm start
```

## Technologies

- Next.js 13+
- React 18+
- TypeScript
- TailwindCSS
- Jest & React Testing Library
