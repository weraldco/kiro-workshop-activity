import { Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';
import { DatabaseService } from '../services/database.service';
import { ValidationService } from '../services/validation.service';
import { Workshop, ErrorResponse } from '../types';

/**
 * Workshop Controller
 * Handles HTTP requests for workshop CRUD operations
 */
export class WorkshopController {
  /**
   * POST /api/workshops
   * Create a new workshop with default status='pending' and signup_enabled=true
   */
  static async createWorkshop(req: Request, res: Response): Promise<void> {
    try {
      const { title, description } = req.body;

      // Validate required fields
      if (!title || typeof title !== 'string') {
        const error: ErrorResponse = {
          error: 'Title is required and must be a string',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      if (!description || typeof description !== 'string') {
        const error: ErrorResponse = {
          error: 'Description is required and must be a string',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      // Create workshop with defaults
      const now = new Date().toISOString();
      const workshop: Workshop = {
        id: uuidv4(),
        title: title.trim(),
        description: description.trim(),
        status: 'pending',
        signup_enabled: true,
        created_at: now,
        updated_at: now
      };

      // Validate workshop schema
      try {
        ValidationService.validateWorkshop(workshop);
      } catch (validationError) {
        const error: ErrorResponse = {
          error: (validationError as Error).message,
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      // Persist to database
      try {
        const workshops = DatabaseService.readWorkshops();
        workshops.push(workshop);
        DatabaseService.writeWorkshops(workshops);
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to persist workshop data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      res.status(201).json(workshop);
    } catch (error) {
      const errorResponse: ErrorResponse = {
        error: 'Internal server error',
        code: 'INTERNAL_ERROR',
        status: 500
      };
      res.status(500).json(errorResponse);
    }
  }

  /**
   * GET /api/workshops
   * List all workshops
   */
  static async listWorkshops(_req: Request, res: Response): Promise<void> {
    try {
      const workshops = DatabaseService.readWorkshops();
      // Return array directly for simpler API (matches design document)
      res.status(200).json(workshops);
    } catch (error) {
      const errorResponse: ErrorResponse = {
        error: 'Failed to retrieve workshops',
        code: 'DATABASE_ERROR',
        status: 500
      };
      res.status(500).json(errorResponse);
    }
  }

  /**
   * PATCH /api/workshops/:id/status
   * Update workshop status
   */
  static async updateWorkshopStatus(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const { status } = req.body;

      // Validate status value
      if (!status || typeof status !== 'string') {
        const error: ErrorResponse = {
          error: 'Status is required and must be a string',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      if (status !== 'pending' && status !== 'ongoing' && status !== 'completed') {
        const error: ErrorResponse = {
          error: 'Status must be one of: pending, ongoing, completed',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      // Read workshops
      let workshops: Workshop[];
      try {
        workshops = DatabaseService.readWorkshops();
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to read workshop data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      // Find workshop
      const workshopIndex = workshops.findIndex(w => w.id === id);
      if (workshopIndex === -1) {
        const error: ErrorResponse = {
          error: `Workshop with id '${id}' not found`,
          code: 'WORKSHOP_NOT_FOUND',
          status: 404
        };
        res.status(404).json(error);
        return;
      }

      // Update status
      workshops[workshopIndex].status = status as 'pending' | 'ongoing' | 'completed';
      workshops[workshopIndex].updated_at = new Date().toISOString();

      // Persist changes
      try {
        DatabaseService.writeWorkshops(workshops);
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to persist workshop data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      res.status(200).json(workshops[workshopIndex]);
    } catch (error) {
      const errorResponse: ErrorResponse = {
        error: 'Internal server error',
        code: 'INTERNAL_ERROR',
        status: 500
      };
      res.status(500).json(errorResponse);
    }
  }

  /**
   * PATCH /api/workshops/:id/signup-flag
   * Toggle signup_enabled flag
   */
  static async updateSignupFlag(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const { signup_enabled } = req.body;

      // Validate signup_enabled value
      if (typeof signup_enabled !== 'boolean') {
        const error: ErrorResponse = {
          error: 'signup_enabled is required and must be a boolean',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      // Read workshops
      let workshops: Workshop[];
      try {
        workshops = DatabaseService.readWorkshops();
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to read workshop data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      // Find workshop
      const workshopIndex = workshops.findIndex(w => w.id === id);
      if (workshopIndex === -1) {
        const error: ErrorResponse = {
          error: `Workshop with id '${id}' not found`,
          code: 'WORKSHOP_NOT_FOUND',
          status: 404
        };
        res.status(404).json(error);
        return;
      }

      // Update signup flag
      workshops[workshopIndex].signup_enabled = signup_enabled;
      workshops[workshopIndex].updated_at = new Date().toISOString();

      // Persist changes
      try {
        DatabaseService.writeWorkshops(workshops);
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to persist workshop data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      res.status(200).json(workshops[workshopIndex]);
    } catch (error) {
      const errorResponse: ErrorResponse = {
        error: 'Internal server error',
        code: 'INTERNAL_ERROR',
        status: 500
      };
      res.status(500).json(errorResponse);
    }
  }
}
