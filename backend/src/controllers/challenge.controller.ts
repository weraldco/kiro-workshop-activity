import { Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';
import { DatabaseService } from '../services/database.service';
import { AccessControlService } from '../services/access-control.service';
import { ValidationService } from '../services/validation.service';
import { ReferentialIntegrityService } from '../services/referential-integrity.service';
import { Challenge, ErrorResponse } from '../types';

/**
 * Challenge Controller
 * Handles HTTP requests for challenge operations with access control
 * Requirements: 3.1, 3.2, 3.3, 3.4, 5.1, 5.2, 5.3, 5.4, 5.5
 */
export class ChallengeController {
  /**
   * POST /api/workshops/:id/challenges
   * Create a challenge for a workshop
   * Requirements: 5.1, 5.2, 5.3, 5.4, 5.5
   */
  static async createChallenge(req: Request, res: Response): Promise<void> {
    try {
      const { id: workshopId } = req.params;
      const { title, description, html_content } = req.body;

      // Validate required fields
      if (!title || typeof title !== 'string') {
        const error: ErrorResponse = {
          error: 'title is required and must be a string',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      if (!description || typeof description !== 'string') {
        const error: ErrorResponse = {
          error: 'description is required and must be a string',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      if (!html_content || typeof html_content !== 'string') {
        const error: ErrorResponse = {
          error: 'html_content is required and must be a string',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      // Validate field lengths (Requirements 5.1, 5.2)
      if (title.length === 0 || title.length > 200) {
        const error: ErrorResponse = {
          error: 'Challenge title must be between 1 and 200 characters',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      if (description.length === 0 || description.length > 1000) {
        const error: ErrorResponse = {
          error: 'Challenge description must be between 1 and 1000 characters',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      // Verify workshop exists (Requirement 5.4 - referential integrity)
      if (!ReferentialIntegrityService.workshopExists(workshopId)) {
        const error: ErrorResponse = {
          error: `Workshop with id '${workshopId}' not found`,
          code: 'WORKSHOP_NOT_FOUND',
          status: 404
        };
        res.status(404).json(error);
        return;
      }

      // Create challenge
      const challenge: Challenge = {
        id: uuidv4(),
        workshop_id: workshopId,
        title: title.trim(),
        description: description.trim(),
        html_content: html_content
      };

      // Validate challenge schema (includes HTML validation - Requirement 5.3)
      try {
        ValidationService.validateChallenge(challenge);
      } catch (validationError) {
        const error: ErrorResponse = {
          error: (validationError as Error).message,
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      // Persist to database (Requirement 5.5)
      try {
        const challenges = DatabaseService.readChallenges();
        challenges.push(challenge);
        DatabaseService.writeChallenges(challenges);
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to persist challenge data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      res.status(201).json({
        success: true,
        challenge_id: challenge.id,
        challenge: challenge
      });
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
   * GET /api/workshops/:id/challenges
   * List challenges for a workshop with access control
   * Requirements: 3.1, 3.2, 3.3, 3.4
   */
  static async listChallenges(req: Request, res: Response): Promise<void> {
    try {
      const { id: workshopId } = req.params;
      const { user_id } = req.query;

      // Validate user_id
      if (!user_id || typeof user_id !== 'string' || user_id.trim() === '') {
        const error: ErrorResponse = {
          error: 'user_id query parameter is required',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      // Read workshop
      let workshops;
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

      const workshop = workshops.find(w => w.id === workshopId);
      if (!workshop) {
        const error: ErrorResponse = {
          error: `Workshop with id '${workshopId}' not found`,
          code: 'WORKSHOP_NOT_FOUND',
          status: 404
        };
        res.status(404).json(error);
        return;
      }

      // Check access control (Requirements 3.1, 3.2, 3.3, 3.4)
      if (!AccessControlService.canAccessChallenges(workshop, user_id)) {
        let errorMessage = 'Access to challenges is not allowed';
        
        if (workshop.status === 'pending') {
          errorMessage = 'Challenges are not accessible for pending workshops';
        } else if (workshop.status === 'completed') {
          errorMessage = 'Challenges are not accessible for completed workshops';
        } else if (!AccessControlService.isParticipant(workshopId, user_id)) {
          errorMessage = 'Only participants can access challenges';
        }

        const error: ErrorResponse = {
          error: errorMessage,
          code: 'CHALLENGE_ACCESS_DENIED',
          status: 403
        };
        res.status(403).json(error);
        return;
      }

      // Read and filter challenges
      let challenges;
      try {
        challenges = DatabaseService.readChallenges();
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to read challenge data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      const workshopChallenges = challenges.filter(
        c => c.workshop_id === workshopId
      );

      res.status(200).json({ challenges: workshopChallenges });
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
   * GET /api/challenges/:id
   * Get challenge details with access control
   * Requirements: 3.1, 3.2, 3.3, 3.4
   */
  static async getChallengeById(req: Request, res: Response): Promise<void> {
    try {
      const { id: challengeId } = req.params;
      const { user_id } = req.query;

      // Validate user_id
      if (!user_id || typeof user_id !== 'string' || user_id.trim() === '') {
        const error: ErrorResponse = {
          error: 'user_id query parameter is required',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      // Read challenge
      let challenges;
      try {
        challenges = DatabaseService.readChallenges();
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to read challenge data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      const challenge = challenges.find(c => c.id === challengeId);
      if (!challenge) {
        const error: ErrorResponse = {
          error: `Challenge with id '${challengeId}' not found`,
          code: 'CHALLENGE_NOT_FOUND',
          status: 404
        };
        res.status(404).json(error);
        return;
      }

      // Read workshop to check access control
      let workshops;
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

      const workshop = workshops.find(w => w.id === challenge.workshop_id);
      if (!workshop) {
        const error: ErrorResponse = {
          error: `Workshop with id '${challenge.workshop_id}' not found`,
          code: 'WORKSHOP_NOT_FOUND',
          status: 404
        };
        res.status(404).json(error);
        return;
      }

      // Check access control (Requirements 3.1, 3.2, 3.3, 3.4)
      if (!AccessControlService.canAccessChallenges(workshop, user_id)) {
        let errorMessage = 'Access to challenge is not allowed';
        
        if (workshop.status === 'pending') {
          errorMessage = 'Challenges are not accessible for pending workshops';
        } else if (workshop.status === 'completed') {
          errorMessage = 'Challenges are not accessible for completed workshops';
        } else if (!AccessControlService.isParticipant(challenge.workshop_id, user_id)) {
          errorMessage = 'Only participants can access challenges';
        }

        const error: ErrorResponse = {
          error: errorMessage,
          code: 'CHALLENGE_ACCESS_DENIED',
          status: 403
        };
        res.status(403).json(error);
        return;
      }

      res.status(200).json({ challenge });
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
