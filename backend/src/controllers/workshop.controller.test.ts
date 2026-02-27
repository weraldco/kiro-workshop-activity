import request from 'supertest';
import app from '../app';
import { DatabaseService } from '../services/database.service';
import { Workshop } from '../types';

// Mock the DatabaseService
jest.mock('../services/database.service');

describe('WorkshopController', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('POST /api/workshops', () => {
    it('should create a workshop with valid data', async () => {
      const mockWorkshops: Workshop[] = [];
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue(mockWorkshops);
      (DatabaseService.writeWorkshops as jest.Mock).mockImplementation(() => {});

      const response = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'This is a test workshop'
        });

      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('id');
      expect(response.body.title).toBe('Test Workshop');
      expect(response.body.description).toBe('This is a test workshop');
      expect(response.body.status).toBe('pending');
      expect(response.body.signup_enabled).toBe(true);
      expect(response.body).toHaveProperty('created_at');
      expect(response.body).toHaveProperty('updated_at');
    });

    it('should reject workshop creation with missing title', async () => {
      const response = await request(app)
        .post('/api/workshops')
        .send({
          description: 'This is a test workshop'
        });

      expect(response.status).toBe(400);
      expect(response.body.error).toContain('Title is required');
      expect(response.body.code).toBe('VALIDATION_ERROR');
    });

    it('should reject workshop creation with missing description', async () => {
      const response = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop'
        });

      expect(response.status).toBe(400);
      expect(response.body.error).toContain('Description is required');
      expect(response.body.code).toBe('VALIDATION_ERROR');
    });

    it('should reject workshop with title exceeding 200 characters', async () => {
      const longTitle = 'a'.repeat(201);
      const response = await request(app)
        .post('/api/workshops')
        .send({
          title: longTitle,
          description: 'Valid description'
        });

      expect(response.status).toBe(400);
      expect(response.body.error).toContain('title must be between 1 and 200 characters');
      expect(response.body.code).toBe('VALIDATION_ERROR');
    });

    it('should reject workshop with description exceeding 1000 characters', async () => {
      const longDescription = 'a'.repeat(1001);
      const response = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Valid Title',
          description: longDescription
        });

      expect(response.status).toBe(400);
      expect(response.body.error).toContain('description must be between 1 and 1000 characters');
      expect(response.body.code).toBe('VALIDATION_ERROR');
    });

    it('should handle database write errors', async () => {
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([]);
      (DatabaseService.writeWorkshops as jest.Mock).mockImplementation(() => {
        throw new Error('Database write failed');
      });

      const response = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'This is a test workshop'
        });

      expect(response.status).toBe(500);
      expect(response.body.error).toBe('Failed to persist workshop data');
      expect(response.body.code).toBe('DATABASE_ERROR');
    });
  });

  describe('GET /api/workshops', () => {
    it('should return all workshops', async () => {
      const mockWorkshops: Workshop[] = [
        {
          id: '123e4567-e89b-12d3-a456-426614174000',
          title: 'Workshop 1',
          description: 'Description 1',
          status: 'pending',
          signup_enabled: true,
          created_at: '2024-01-01T00:00:00.000Z',
          updated_at: '2024-01-01T00:00:00.000Z'
        },
        {
          id: '123e4567-e89b-12d3-a456-426614174001',
          title: 'Workshop 2',
          description: 'Description 2',
          status: 'ongoing',
          signup_enabled: false,
          created_at: '2024-01-02T00:00:00.000Z',
          updated_at: '2024-01-02T00:00:00.000Z'
        }
      ];

      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue(mockWorkshops);

      const response = await request(app).get('/api/workshops');

      expect(response.status).toBe(200);
      expect(response.body).toHaveLength(2);
      expect(response.body[0].title).toBe('Workshop 1');
      expect(response.body[1].title).toBe('Workshop 2');
    });

    it('should return empty array when no workshops exist', async () => {
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([]);

      const response = await request(app).get('/api/workshops');

      expect(response.status).toBe(200);
      expect(response.body).toEqual([]);
    });

    it('should handle database read errors', async () => {
      (DatabaseService.readWorkshops as jest.Mock).mockImplementation(() => {
        throw new Error('Database read failed');
      });

      const response = await request(app).get('/api/workshops');

      expect(response.status).toBe(500);
      expect(response.body.error).toBe('Failed to retrieve workshops');
      expect(response.body.code).toBe('DATABASE_ERROR');
    });
  });

  describe('PATCH /api/workshops/:id/status', () => {
    const mockWorkshop: Workshop = {
      id: '123e4567-e89b-12d3-a456-426614174000',
      title: 'Test Workshop',
      description: 'Test Description',
      status: 'pending',
      signup_enabled: true,
      created_at: '2024-01-01T00:00:00.000Z',
      updated_at: '2024-01-01T00:00:00.000Z'
    };

    it('should update workshop status from pending to ongoing', async () => {
      const oldTimestamp = '2024-01-01T00:00:00.000Z';
      const workshopToUpdate = { ...mockWorkshop, updated_at: oldTimestamp };
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([workshopToUpdate]);
      (DatabaseService.writeWorkshops as jest.Mock).mockImplementation(() => {});

      const response = await request(app)
        .patch(`/api/workshops/${mockWorkshop.id}/status`)
        .send({ status: 'ongoing' });

      expect(response.status).toBe(200);
      expect(response.body.status).toBe('ongoing');
      expect(response.body.updated_at).not.toBe(oldTimestamp);
    });

    it('should update workshop status from ongoing to completed', async () => {
      const ongoingWorkshop = { ...mockWorkshop, status: 'ongoing' as const };
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([ongoingWorkshop]);
      (DatabaseService.writeWorkshops as jest.Mock).mockImplementation(() => {});

      const response = await request(app)
        .patch(`/api/workshops/${mockWorkshop.id}/status`)
        .send({ status: 'completed' });

      expect(response.status).toBe(200);
      expect(response.body.status).toBe('completed');
    });

    it('should reject invalid status values', async () => {
      const response = await request(app)
        .patch(`/api/workshops/${mockWorkshop.id}/status`)
        .send({ status: 'invalid' });

      expect(response.status).toBe(400);
      expect(response.body.error).toContain('Status must be one of: pending, ongoing, completed');
      expect(response.body.code).toBe('VALIDATION_ERROR');
    });

    it('should return 404 for non-existent workshop', async () => {
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([]);

      const response = await request(app)
        .patch('/api/workshops/non-existent-id/status')
        .send({ status: 'ongoing' });

      expect(response.status).toBe(404);
      expect(response.body.error).toContain('Workshop with id');
      expect(response.body.code).toBe('WORKSHOP_NOT_FOUND');
    });

    it('should reject missing status field', async () => {
      const response = await request(app)
        .patch(`/api/workshops/${mockWorkshop.id}/status`)
        .send({});

      expect(response.status).toBe(400);
      expect(response.body.error).toContain('Status is required');
      expect(response.body.code).toBe('VALIDATION_ERROR');
    });
  });

  describe('PATCH /api/workshops/:id/signup-flag', () => {
    const mockWorkshop: Workshop = {
      id: '123e4567-e89b-12d3-a456-426614174000',
      title: 'Test Workshop',
      description: 'Test Description',
      status: 'pending',
      signup_enabled: true,
      created_at: '2024-01-01T00:00:00.000Z',
      updated_at: '2024-01-01T00:00:00.000Z'
    };

    it('should toggle signup_enabled from true to false', async () => {
      const oldTimestamp = '2024-01-01T00:00:00.000Z';
      const workshopToUpdate = { ...mockWorkshop, updated_at: oldTimestamp };
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([workshopToUpdate]);
      (DatabaseService.writeWorkshops as jest.Mock).mockImplementation(() => {});

      const response = await request(app)
        .patch(`/api/workshops/${mockWorkshop.id}/signup-flag`)
        .send({ signup_enabled: false });

      expect(response.status).toBe(200);
      expect(response.body.signup_enabled).toBe(false);
      expect(response.body.updated_at).not.toBe(oldTimestamp);
    });

    it('should toggle signup_enabled from false to true', async () => {
      const workshopWithSignupDisabled = { ...mockWorkshop, signup_enabled: false };
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([workshopWithSignupDisabled]);
      (DatabaseService.writeWorkshops as jest.Mock).mockImplementation(() => {});

      const response = await request(app)
        .patch(`/api/workshops/${mockWorkshop.id}/signup-flag`)
        .send({ signup_enabled: true });

      expect(response.status).toBe(200);
      expect(response.body.signup_enabled).toBe(true);
    });

    it('should reject non-boolean signup_enabled values', async () => {
      const response = await request(app)
        .patch(`/api/workshops/${mockWorkshop.id}/signup-flag`)
        .send({ signup_enabled: 'true' });

      expect(response.status).toBe(400);
      expect(response.body.error).toContain('signup_enabled is required and must be a boolean');
      expect(response.body.code).toBe('VALIDATION_ERROR');
    });

    it('should return 404 for non-existent workshop', async () => {
      (DatabaseService.readWorkshops as jest.Mock).mockReturnValue([]);

      const response = await request(app)
        .patch('/api/workshops/non-existent-id/signup-flag')
        .send({ signup_enabled: false });

      expect(response.status).toBe(404);
      expect(response.body.error).toContain('Workshop with id');
      expect(response.body.code).toBe('WORKSHOP_NOT_FOUND');
    });

    it('should reject missing signup_enabled field', async () => {
      const response = await request(app)
        .patch(`/api/workshops/${mockWorkshop.id}/signup-flag`)
        .send({});

      expect(response.status).toBe(400);
      expect(response.body.error).toContain('signup_enabled is required');
      expect(response.body.code).toBe('VALIDATION_ERROR');
    });
  });
});
