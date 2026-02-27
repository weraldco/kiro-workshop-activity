import express, { Application, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import workshopRoutes from './routes/workshop.routes';
import { ErrorResponse } from './types';

const app: Application = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req: Request, _res: Response, next: NextFunction) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// API routes
app.use('/api', workshopRoutes);

// Health check endpoint
app.get('/health', (_req: Request, res: Response) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 404 handler
app.use((_req: Request, res: Response) => {
  const error: ErrorResponse = {
    error: 'Endpoint not found',
    code: 'NOT_FOUND',
    status: 404
  };
  res.status(404).json(error);
});

// Global error handler
app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  console.error('Unhandled error:', err);
  const error: ErrorResponse = {
    error: 'Internal server error',
    code: 'INTERNAL_ERROR',
    status: 500
  };
  res.status(500).json(error);
});

export default app;
