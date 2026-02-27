import { Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';
import { DatabaseService } from '../services/database.service';
import { AccessControlService } from '../services/access-control.service';
import { ValidationService } from '../services/validation.service';
import { Participant, ErrorResponse } from '../types';

/**
 * Participant Controller
 * Handles HTTP requests for participant signup operations
 */
export class ParticipantController {
  /**
   * POST /api/workshops/:id/signup
   * Register a participant for a workshop
   * Requirements: 2.1, 2.2, 2.3, 2.4
   */
  static async signup(req: Request, res: Response): Promise<void> {
    try {
      const { id: workshopId } = req.params;
      const { user_id } = req.body;

      // Validate user_id
      if (!user_id || typeof user_id !== 'string' || user_id.trim() === '') {
        const error: ErrorResponse = {
          error: 'user_id is required and must be a non-empty string',
          code: 'VALIDATION_ERROR',
          status: 400
        };
        res.status(400).json(error);
        return;
      }

      // Read workshops
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

      // Find workshop
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

      // Check if signup is allowed using Access Control Service
      if (!AccessControlService.canSignup(workshop)) {
        let errorMessage = 'Signups are not allowed for this workshop';
        
        if (!workshop.signup_enabled) {
          errorMessage = 'Signups are disabled for this workshop';
        } else if (workshop.status === 'ongoing') {
          errorMessage = "Signups are not allowed for workshops with status 'ongoing'";
        } else if (workshop.status === 'completed') {
          errorMessage = "Signups are not allowed for workshops with status 'completed'";
        }

        const error: ErrorResponse = {
          error: errorMessage,
          code: 'SIGNUP_NOT_ALLOWED',
          status: 403
        };
        res.status(403).json(error);
        return;
      }

      // Read participants
      let participants;
      try {
        participants = DatabaseService.readParticipants();
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to read participant data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      // Check for duplicate signup (uniqueness constraint on workshop_id + user_id)
      const existingParticipant = participants.find(
        p => p.workshop_id === workshopId && p.user_id === user_id.trim()
      );

      if (existingParticipant) {
        const error: ErrorResponse = {
          error: 'User is already signed up for this workshop',
          code: 'DUPLICATE_SIGNUP',
          status: 403
        };
        res.status(403).json(error);
        return;
      }

      // Create participant
      const participant: Participant = {
        id: uuidv4(),
        workshop_id: workshopId,
        user_id: user_id.trim(),
        signed_up_at: new Date().toISOString()
      };

      // Validate participant schema
      try {
        ValidationService.validateParticipant(participant);
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
        participants.push(participant);
        DatabaseService.writeParticipants(participants);
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to persist participant data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      res.status(200).json({
        success: true,
        participant_id: participant.id
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
   * GET /api/workshops/:id/participants
   * List all participants for a workshop
   */
  static async listParticipants(req: Request, res: Response): Promise<void> {
    try {
      const { id: workshopId } = req.params;

      // Verify workshop exists
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

      // Read and filter participants
      let participants;
      try {
        participants = DatabaseService.readParticipants();
      } catch (dbError) {
        const error: ErrorResponse = {
          error: 'Failed to read participant data',
          code: 'DATABASE_ERROR',
          status: 500
        };
        res.status(500).json(error);
        return;
      }

      const workshopParticipants = participants.filter(
        p => p.workshop_id === workshopId
      );

      res.status(200).json({ participants: workshopParticipants });
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
