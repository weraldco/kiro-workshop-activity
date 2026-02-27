import { Request, Response } from 'express';
import { ParticipantController } from './participant.controller';
import { DatabaseService } from '../services/database.service';
import { ValidationService } from '../services/validation.service';
import { Workshop, Participant } from '../types';

// Mock the services
jest.mock('../services/database.service');
jest.mock('../services/validation.service');

describe('ParticipantController', () => {
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let responseJson: jest.Mock;
  let responseStatus: jest.Mock;

  beforeEach(() => {
    responseJson = jest.fn();
    responseStatus = jest.fn().mockReturnValue({ json: responseJson });
    
    mockRequest = {
      params: {},
      body: {}
    };
    
    mockResponse = {
      status: responseStatus,
      json: responseJson
    };

    jest.clearAllMocks();
    
    // Mock ValidationService to not throw errors by default
    (ValidationService.validateParticipant as jest.Mock).mockImplementation(() => {});
  });

  describe('signup', () => {
    const mockWorkshop: Workshop = {
      id: 'workshop-1',
      title: 'Test Workshop',
      description: 'Test Description',
      status: 'pending',
      signup_enabled: true,
      created_at: '2024-01-01T00:00:00.000Z',
      updated_at: '2024-01-01T00:00:00.000Z'
    };

    it('should successfully register a participant for a pending workshop with signup enabled', async () => {
      mockRequest.params = { id: 'workshop-1' };
      mockRequest.body = { user_id: 'user-123' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([mockWorkshop]);
      (DatabaseService.readParticipants as jest.Mock).mockReturnValue([]);
      (DatabaseService.writeParticipants as jest.Mock).mockImplementation(() => {});

      await ParticipantController.signup(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(200);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          success: true,
          participant_id: expect.any(String)
        })
      );
      expect(DatabaseService.writeParticipants).toHaveBeenCalled();
    });

    it('should reject signup when user_id is missing', async () => {
      mockRequest.params = { id: 'workshop-1' };
      mockRequest.body = {};

      await ParticipantController.signup(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(400);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'user_id is required and must be a non-empty string',
          code: 'VALIDATION_ERROR'
        })
      );
    });

    it('should reject signup when user_id is empty string', async () => {
      mockRequest.params = { id: 'workshop-1' };
      mockRequest.body = { user_id: '   ' };

      await ParticipantController.signup(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(400);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'user_id is required and must be a non-empty string',
          code: 'VALIDATION_ERROR'
        })
      );
    });

    it('should return 404 when workshop does not exist', async () => {
      mockRequest.params = { id: 'non-existent' };
      mockRequest.body = { user_id: 'user-123' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([]);

      await ParticipantController.signup(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(404);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: "Workshop with id 'non-existent' not found",
          code: 'WORKSHOP_NOT_FOUND'
        })
      );
    });

    it('should reject signup for ongoing workshop', async () => {
      const ongoingWorkshop = { ...mockWorkshop, status: 'ongoing' as const };
      mockRequest.params = { id: 'workshop-1' };
      mockRequest.body = { user_id: 'user-123' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([ongoingWorkshop]);

      await ParticipantController.signup(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(403);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: "Signups are not allowed for workshops with status 'ongoing'",
          code: 'SIGNUP_NOT_ALLOWED'
        })
      );
    });

    it('should reject signup for completed workshop', async () => {
      const completedWorkshop = { ...mockWorkshop, status: 'completed' as const };
      mockRequest.params = { id: 'workshop-1' };
      mockRequest.body = { user_id: 'user-123' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([completedWorkshop]);

      await ParticipantController.signup(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(403);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: "Signups are not allowed for workshops with status 'completed'",
          code: 'SIGNUP_NOT_ALLOWED'
        })
      );
    });

    it('should reject signup when signup_enabled is false', async () => {
      const disabledWorkshop = { ...mockWorkshop, signup_enabled: false };
      mockRequest.params = { id: 'workshop-1' };
      mockRequest.body = { user_id: 'user-123' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([disabledWorkshop]);

      await ParticipantController.signup(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(403);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Signups are disabled for this workshop',
          code: 'SIGNUP_NOT_ALLOWED'
        })
      );
    });

    it('should reject duplicate signup for same user and workshop', async () => {
      const existingParticipant: Participant = {
        id: 'participant-1',
        workshop_id: 'workshop-1',
        user_id: 'user-123',
        signed_up_at: '2024-01-01T00:00:00.000Z'
      };

      mockRequest.params = { id: 'workshop-1' };
      mockRequest.body = { user_id: 'user-123' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([mockWorkshop]);
      (DatabaseService.readParticipants as jest.Mock).mockReturnValue([existingParticipant]);

      await ParticipantController.signup(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(403);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'User is already signed up for this workshop',
          code: 'DUPLICATE_SIGNUP'
        })
      );
    });

    it('should handle database read errors gracefully', async () => {
      mockRequest.params = { id: 'workshop-1' };
      mockRequest.body = { user_id: 'user-123' };

      (DatabaseService.readWorkshops as jest.Mock).mockImplementation(() => {
        throw new Error('Database read failed');
      });

      await ParticipantController.signup(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(500);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Failed to read workshop data',
          code: 'DATABASE_ERROR'
        })
      );
    });

    it('should handle database write errors gracefully', async () => {
      mockRequest.params = { id: 'workshop-1' };
      mockRequest.body = { user_id: 'user-123' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([mockWorkshop]);
      (DatabaseService.readParticipants as jest.Mock).mockReturnValue([]);
      (DatabaseService.writeParticipants as jest.Mock).mockImplementation(() => {
        throw new Error('Database write failed');
      });

      await ParticipantController.signup(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(500);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Failed to persist participant data',
          code: 'DATABASE_ERROR'
        })
      );
    });
  });

  describe('listParticipants', () => {
    const mockWorkshop: Workshop = {
      id: 'workshop-1',
      title: 'Test Workshop',
      description: 'Test Description',
      status: 'pending',
      signup_enabled: true,
      created_at: '2024-01-01T00:00:00.000Z',
      updated_at: '2024-01-01T00:00:00.000Z'
    };

    const mockParticipants: Participant[] = [
      {
        id: 'participant-1',
        workshop_id: 'workshop-1',
        user_id: 'user-123',
        signed_up_at: '2024-01-01T00:00:00.000Z'
      },
      {
        id: 'participant-2',
        workshop_id: 'workshop-1',
        user_id: 'user-456',
        signed_up_at: '2024-01-01T01:00:00.000Z'
      },
      {
        id: 'participant-3',
        workshop_id: 'workshop-2',
        user_id: 'user-789',
        signed_up_at: '2024-01-01T02:00:00.000Z'
      }
    ];

    it('should return all participants for a workshop', async () => {
      mockRequest.params = { id: 'workshop-1' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([mockWorkshop]);
      (DatabaseService.readParticipants as jest.Mock).mockReturnValue(mockParticipants);

      await ParticipantController.listParticipants(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(200);
      expect(responseJson).toHaveBeenCalledWith({
        participants: [mockParticipants[0], mockParticipants[1]]
      });
    });

    it('should return empty array when workshop has no participants', async () => {
      mockRequest.params = { id: 'workshop-1' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([mockWorkshop]);
      (DatabaseService.readParticipants as jest.Mock).mockReturnValue([]);

      await ParticipantController.listParticipants(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(200);
      expect(responseJson).toHaveBeenCalledWith({
        participants: []
      });
    });

    it('should return 404 when workshop does not exist', async () => {
      mockRequest.params = { id: 'non-existent' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([]);

      await ParticipantController.listParticipants(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(404);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: "Workshop with id 'non-existent' not found",
          code: 'WORKSHOP_NOT_FOUND'
        })
      );
    });

    it('should handle database read errors gracefully', async () => {
      mockRequest.params = { id: 'workshop-1' };

      (DatabaseService.readWorkshops as jest.Mock).mockImplementation(() => {
        throw new Error('Database read failed');
      });

      await ParticipantController.listParticipants(mockRequest as Request, mockResponse as Response);

      expect(responseStatus).toHaveBeenCalledWith(500);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Failed to read workshop data',
          code: 'DATABASE_ERROR'
        })
      );
    });
  });
});
