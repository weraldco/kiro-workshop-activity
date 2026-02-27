import { Request, Response } from 'express';
import { ChallengeController } from './challenge.controller';
import { DatabaseService } from '../services/database.service';
import { AccessControlService } from '../services/access-control.service';
import { ValidationService } from '../services/validation.service';
import { ReferentialIntegrityService } from '../services/referential-integrity.service';
import { Workshop, Challenge } from '../types';

// Mock dependencies
jest.mock('../services/database.service');
jest.mock('../services/access-control.service');
jest.mock('../services/validation.service');
jest.mock('../services/referential-integrity.service');

describe('ChallengeController', () => {
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let responseJson: jest.Mock;
  let responseStatus: jest.Mock;

  beforeEach(() => {
    responseJson = jest.fn().mockReturnThis();
    responseStatus = jest.fn().mockReturnThis();

    mockRequest = {
      params: {},
      body: {},
      query: {}
    };

    mockResponse = {
      status: responseStatus,
      json: responseJson
    };

    jest.clearAllMocks();
  });

  describe('createChallenge', () => {
    const validChallenge = {
      title: 'Test Challenge',
      description: 'Test description',
      html_content: '<p>Test HTML content</p>'
    };

    it('should create a challenge with valid data', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.body = validChallenge;

      (ReferentialIntegrityService.workshopExists as jest.Mock).mockReturnValue(true);
      (ValidationService.validateChallenge as jest.Mock).mockImplementation(() => {});
      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([]);
      (DatabaseService.writeChallenges as jest.Mock).mockImplementation(() => {});

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(201);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          success: true,
          challenge_id: expect.any(String),
          challenge: expect.objectContaining({
            id: expect.any(String),
            workshop_id: 'workshop-123',
            title: 'Test Challenge',
            description: 'Test description',
            html_content: '<p>Test HTML content</p>'
          })
        })
      );
    });

    it('should reject challenge with missing title', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.body = {
        description: 'Test description',
        html_content: '<p>Test HTML</p>'
      };

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(400);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'title is required and must be a string',
          code: 'VALIDATION_ERROR'
        })
      );
    });

    it('should reject challenge with missing description', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.body = {
        title: 'Test Challenge',
        html_content: '<p>Test HTML</p>'
      };

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(400);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'description is required and must be a string',
          code: 'VALIDATION_ERROR'
        })
      );
    });

    it('should reject challenge with missing html_content', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.body = {
        title: 'Test Challenge',
        description: 'Test description'
      };

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(400);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'html_content is required and must be a string',
          code: 'VALIDATION_ERROR'
        })
      );
    });

    it('should reject challenge with title exceeding 200 characters', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.body = {
        title: 'a'.repeat(201),
        description: 'Test description',
        html_content: '<p>Test HTML</p>'
      };

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(400);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Challenge title must be between 1 and 200 characters',
          code: 'VALIDATION_ERROR'
        })
      );
    });

    it('should accept challenge with title exactly 200 characters', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.body = {
        title: 'a'.repeat(200),
        description: 'Test description',
        html_content: '<p>Test HTML</p>'
      };

      (ReferentialIntegrityService.workshopExists as jest.Mock).mockReturnValue(true);
      (ValidationService.validateChallenge as jest.Mock).mockImplementation(() => {});
      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([]);
      (DatabaseService.writeChallenges as jest.Mock).mockImplementation(() => {});

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(201);
    });

    it('should reject challenge with description exceeding 1000 characters', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.body = {
        title: 'Test Challenge',
        description: 'a'.repeat(1001),
        html_content: '<p>Test HTML</p>'
      };

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(400);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Challenge description must be between 1 and 1000 characters',
          code: 'VALIDATION_ERROR'
        })
      );
    });

    it('should accept challenge with description exactly 1000 characters', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.body = {
        title: 'Test Challenge',
        description: 'a'.repeat(1000),
        html_content: '<p>Test HTML</p>'
      };

      (ReferentialIntegrityService.workshopExists as jest.Mock).mockReturnValue(true);
      (ValidationService.validateChallenge as jest.Mock).mockImplementation(() => {});
      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([]);
      (DatabaseService.writeChallenges as jest.Mock).mockImplementation(() => {});

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(201);
    });

    it('should reject challenge with non-existent workshop_id', async () => {
      mockRequest.params = { id: 'non-existent-workshop' };
      mockRequest.body = validChallenge;

      (ReferentialIntegrityService.workshopExists as jest.Mock).mockReturnValue(false);

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(404);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: "Workshop with id 'non-existent-workshop' not found",
          code: 'WORKSHOP_NOT_FOUND'
        })
      );
    });

    it('should reject challenge with invalid HTML content', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.body = {
        title: 'Test Challenge',
        description: 'Test description',
        html_content: '<p>Unclosed tag'
      };

      (ReferentialIntegrityService.workshopExists as jest.Mock).mockReturnValue(true);
      (ValidationService.validateChallenge as jest.Mock).mockImplementation(() => {
        throw new Error('Challenge html_content must be valid HTML');
      });

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(400);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Challenge html_content must be valid HTML',
          code: 'VALIDATION_ERROR'
        })
      );
    });

    it('should handle database write errors', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.body = validChallenge;

      (ReferentialIntegrityService.workshopExists as jest.Mock).mockReturnValue(true);
      (ValidationService.validateChallenge as jest.Mock).mockImplementation(() => {});
      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([]);
      (DatabaseService.writeChallenges as jest.Mock).mockImplementation(() => {
        throw new Error('Write failed');
      });

      await ChallengeController.createChallenge(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(500);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Failed to persist challenge data',
          code: 'DATABASE_ERROR'
        })
      );
    });
  });

  describe('listChallenges', () => {
    const mockWorkshop: Workshop = {
      id: 'workshop-123',
      title: 'Test Workshop',
      description: 'Test description',
      status: 'ongoing',
      signup_enabled: true,
      created_at: '2024-01-01T00:00:00.000Z',
      updated_at: '2024-01-01T00:00:00.000Z'
    };

    const mockChallenges: Challenge[] = [
      {
        id: 'challenge-1',
        workshop_id: 'workshop-123',
        title: 'Challenge 1',
        description: 'Description 1',
        html_content: '<p>Content 1</p>'
      },
      {
        id: 'challenge-2',
        workshop_id: 'workshop-123',
        title: 'Challenge 2',
        description: 'Description 2',
        html_content: '<p>Content 2</p>'
      }
    ];

    it('should list challenges for ongoing workshop participant', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.query = { user_id: 'user-1' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([mockWorkshop]);
      (AccessControlService.canAccessChallenges as jest.Mock).mockReturnValue(true);
      (DatabaseService.readChallenges as jest.Mock).mockReturnValue(mockChallenges);

      await ChallengeController.listChallenges(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(200);
      expect(responseJson).toHaveBeenCalledWith({
        challenges: mockChallenges
      });
    });

    it('should reject challenge access for pending workshop', async () => {
      const pendingWorkshop = { ...mockWorkshop, status: 'pending' as const };
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.query = { user_id: 'user-1' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([pendingWorkshop]);
      (AccessControlService.canAccessChallenges as jest.Mock).mockReturnValue(false);

      await ChallengeController.listChallenges(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(403);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Challenges are not accessible for pending workshops',
          code: 'CHALLENGE_ACCESS_DENIED'
        })
      );
    });

    it('should reject challenge access for completed workshop', async () => {
      const completedWorkshop = { ...mockWorkshop, status: 'completed' as const };
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.query = { user_id: 'user-1' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([completedWorkshop]);
      (AccessControlService.canAccessChallenges as jest.Mock).mockReturnValue(false);

      await ChallengeController.listChallenges(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(403);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Challenges are not accessible for completed workshops',
          code: 'CHALLENGE_ACCESS_DENIED'
        })
      );
    });

    it('should reject challenge access for non-participant', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.query = { user_id: 'non-participant' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([mockWorkshop]);
      (AccessControlService.canAccessChallenges as jest.Mock).mockReturnValue(false);
      (AccessControlService.isParticipant as jest.Mock).mockReturnValue(false);

      await ChallengeController.listChallenges(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(403);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Only participants can access challenges',
          code: 'CHALLENGE_ACCESS_DENIED'
        })
      );
    });

    it('should reject request without user_id', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.query = {};

      await ChallengeController.listChallenges(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(400);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'user_id query parameter is required',
          code: 'VALIDATION_ERROR'
        })
      );
    });

    it('should return 404 for non-existent workshop', async () => {
      mockRequest.params = { id: 'non-existent' };
      mockRequest.query = { user_id: 'user-1' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([]);

      await ChallengeController.listChallenges(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(404);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: "Workshop with id 'non-existent' not found",
          code: 'WORKSHOP_NOT_FOUND'
        })
      );
    });

    it('should return empty array when workshop has no challenges', async () => {
      mockRequest.params = { id: 'workshop-123' };
      mockRequest.query = { user_id: 'user-1' };

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([mockWorkshop]);
      (AccessControlService.canAccessChallenges as jest.Mock).mockReturnValue(true);
      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([]);

      await ChallengeController.listChallenges(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(200);
      expect(responseJson).toHaveBeenCalledWith({
        challenges: []
      });
    });
  });

  describe('getChallengeById', () => {
    const mockWorkshop: Workshop = {
      id: 'workshop-123',
      title: 'Test Workshop',
      description: 'Test description',
      status: 'ongoing',
      signup_enabled: true,
      created_at: '2024-01-01T00:00:00.000Z',
      updated_at: '2024-01-01T00:00:00.000Z'
    };

    const mockChallenge: Challenge = {
      id: 'challenge-1',
      workshop_id: 'workshop-123',
      title: 'Challenge 1',
      description: 'Description 1',
      html_content: '<p>Content 1</p>'
    };

    it('should get challenge details for authorized participant', async () => {
      mockRequest.params = { id: 'challenge-1' };
      mockRequest.query = { user_id: 'user-1' };

      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([mockChallenge]);
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([mockWorkshop]);
      (AccessControlService.canAccessChallenges as jest.Mock).mockReturnValue(true);

      await ChallengeController.getChallengeById(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(200);
      expect(responseJson).toHaveBeenCalledWith({
        challenge: mockChallenge
      });
    });

    it('should reject challenge access for pending workshop', async () => {
      const pendingWorkshop = { ...mockWorkshop, status: 'pending' as const };
      mockRequest.params = { id: 'challenge-1' };
      mockRequest.query = { user_id: 'user-1' };

      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([mockChallenge]);
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([pendingWorkshop]);
      (AccessControlService.canAccessChallenges as jest.Mock).mockReturnValue(false);

      await ChallengeController.getChallengeById(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(403);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Challenges are not accessible for pending workshops',
          code: 'CHALLENGE_ACCESS_DENIED'
        })
      );
    });

    it('should reject challenge access for completed workshop', async () => {
      const completedWorkshop = { ...mockWorkshop, status: 'completed' as const };
      mockRequest.params = { id: 'challenge-1' };
      mockRequest.query = { user_id: 'user-1' };

      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([mockChallenge]);
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([completedWorkshop]);
      (AccessControlService.canAccessChallenges as jest.Mock).mockReturnValue(false);

      await ChallengeController.getChallengeById(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(403);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Challenges are not accessible for completed workshops',
          code: 'CHALLENGE_ACCESS_DENIED'
        })
      );
    });

    it('should reject challenge access for non-participant', async () => {
      mockRequest.params = { id: 'challenge-1' };
      mockRequest.query = { user_id: 'non-participant' };

      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([mockChallenge]);
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([mockWorkshop]);
      (AccessControlService.canAccessChallenges as jest.Mock).mockReturnValue(false);
      (AccessControlService.isParticipant as jest.Mock).mockReturnValue(false);

      await ChallengeController.getChallengeById(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(403);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'Only participants can access challenges',
          code: 'CHALLENGE_ACCESS_DENIED'
        })
      );
    });

    it('should return 404 for non-existent challenge', async () => {
      mockRequest.params = { id: 'non-existent' };
      mockRequest.query = { user_id: 'user-1' };

      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([]);

      await ChallengeController.getChallengeById(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(404);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: "Challenge with id 'non-existent' not found",
          code: 'CHALLENGE_NOT_FOUND'
        })
      );
    });

    it('should reject request without user_id', async () => {
      mockRequest.params = { id: 'challenge-1' };
      mockRequest.query = {};

      await ChallengeController.getChallengeById(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(400);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: 'user_id query parameter is required',
          code: 'VALIDATION_ERROR'
        })
      );
    });

    it('should return 404 when challenge workshop does not exist', async () => {
      mockRequest.params = { id: 'challenge-1' };
      mockRequest.query = { user_id: 'user-1' };

      (DatabaseService.readChallenges as jest.Mock).mockReturnValue([mockChallenge]);
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([]);

      await ChallengeController.getChallengeById(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(responseStatus).toHaveBeenCalledWith(404);
      expect(responseJson).toHaveBeenCalledWith(
        expect.objectContaining({
          error: "Workshop with id 'workshop-123' not found",
          code: 'WORKSHOP_NOT_FOUND'
        })
      );
    });
  });
});
