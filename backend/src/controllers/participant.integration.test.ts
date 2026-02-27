import request from 'supertest';
import app from '../app';
import { DatabaseService } from '../services/database.service';
import { Workshop, Participant } from '../types';

describe('Participant API Integration Tests', () => {
  const testWorkshop: Workshop = {
    id: '123e4567-e89b-42d3-a456-426614174000', // Valid UUID v4 (note the '4' in position 15)
    title: 'Integration Test Workshop',
    description: 'Workshop for integration testing',
    status: 'pending',
    signup_enabled: true,
    created_at: '2024-01-01T00:00:00.000Z',
    updated_at: '2024-01-01T00:00:00.000Z'
  };

  beforeEach(() => {
    // Clear database before each test
    DatabaseService.writeWorkshops([testWorkshop]);
    DatabaseService.writeParticipants([]);
  });

  afterAll(() => {
    // Clean up database after all tests
    DatabaseService.writeWorkshops([]);
    DatabaseService.writeParticipants([]);
  });

  describe('POST /api/workshops/:id/signup', () => {
    it('should successfully register a participant for a pending workshop', async () => {
      const response = await request(app)
        .post(`/api/workshops/${testWorkshop.id}/signup`)
        .send({ user_id: 'test-user-123' })
        .expect(200);

      expect(response.body).toMatchObject({
        success: true,
        participant_id: expect.any(String)
      });

      // Verify participant was added to database
      const participants = DatabaseService.readParticipants();
      expect(participants).toHaveLength(1);
      expect(participants[0]).toMatchObject({
        workshop_id: testWorkshop.id,
        user_id: 'test-user-123'
      });
    });

    it('should reject signup for ongoing workshop', async () => {
      const ongoingWorkshop = { ...testWorkshop, status: 'ongoing' as const };
      DatabaseService.writeWorkshops([ongoingWorkshop]);

      const response = await request(app)
        .post(`/api/workshops/${testWorkshop.id}/signup`)
        .send({ user_id: 'test-user-123' })
        .expect(403);

      expect(response.body).toMatchObject({
        error: "Signups are not allowed for workshops with status 'ongoing'",
        code: 'SIGNUP_NOT_ALLOWED'
      });
    });

    it('should reject signup for completed workshop', async () => {
      const completedWorkshop = { ...testWorkshop, status: 'completed' as const };
      DatabaseService.writeWorkshops([completedWorkshop]);

      const response = await request(app)
        .post(`/api/workshops/${completedWorkshop.id}/signup`)
        .send({ user_id: 'test-user-123' })
        .expect(403);

      expect(response.body).toMatchObject({
        error: "Signups are not allowed for workshops with status 'completed'",
        code: 'SIGNUP_NOT_ALLOWED'
      });
    });

    it('should reject signup when signup_enabled is false', async () => {
      const disabledWorkshop = { ...testWorkshop, signup_enabled: false };
      DatabaseService.writeWorkshops([disabledWorkshop]);

      const response = await request(app)
        .post(`/api/workshops/${testWorkshop.id}/signup`)
        .send({ user_id: 'test-user-123' })
        .expect(403);

      expect(response.body).toMatchObject({
        error: 'Signups are disabled for this workshop',
        code: 'SIGNUP_NOT_ALLOWED'
      });
    });

    it('should reject duplicate signup', async () => {
      // First signup
      await request(app)
        .post(`/api/workshops/${testWorkshop.id}/signup`)
        .send({ user_id: 'test-user-123' })
        .expect(200);

      // Duplicate signup
      const response = await request(app)
        .post(`/api/workshops/${testWorkshop.id}/signup`)
        .send({ user_id: 'test-user-123' })
        .expect(403);

      expect(response.body).toMatchObject({
        error: 'User is already signed up for this workshop',
        code: 'DUPLICATE_SIGNUP'
      });
    });

    it('should return 404 for non-existent workshop', async () => {
      const response = await request(app)
        .post('/api/workshops/123e4567-e89b-42d3-a456-999999999999/signup')
        .send({ user_id: 'test-user-123' })
        .expect(404);

      expect(response.body).toMatchObject({
        error: expect.stringContaining('not found'),
        code: 'WORKSHOP_NOT_FOUND'
      });
    });

    it('should reject signup with missing user_id', async () => {
      const response = await request(app)
        .post(`/api/workshops/${testWorkshop.id}/signup`)
        .send({})
        .expect(400);

      expect(response.body).toMatchObject({
        error: 'user_id is required and must be a non-empty string',
        code: 'VALIDATION_ERROR'
      });
    });
  });

  describe('GET /api/workshops/:id/participants', () => {
    it('should return all participants for a workshop', async () => {
      const participants: Participant[] = [
        {
          id: '123e4567-e89b-42d3-a456-111111111111',
          workshop_id: testWorkshop.id,
          user_id: 'user-1',
          signed_up_at: '2024-01-01T00:00:00.000Z'
        },
        {
          id: '123e4567-e89b-42d3-a456-222222222222',
          workshop_id: testWorkshop.id,
          user_id: 'user-2',
          signed_up_at: '2024-01-01T01:00:00.000Z'
        }
      ];
      DatabaseService.writeParticipants(participants);

      const response = await request(app)
        .get(`/api/workshops/${testWorkshop.id}/participants`)
        .expect(200);

      expect(response.body).toMatchObject({
        participants: expect.arrayContaining([
          expect.objectContaining({ user_id: 'user-1' }),
          expect.objectContaining({ user_id: 'user-2' })
        ])
      });
      expect(response.body.participants).toHaveLength(2);
    });

    it('should return empty array when workshop has no participants', async () => {
      const response = await request(app)
        .get(`/api/workshops/${testWorkshop.id}/participants`)
        .expect(200);

      expect(response.body).toEqual({
        participants: []
      });
    });

    it('should return 404 for non-existent workshop', async () => {
      const response = await request(app)
        .get('/api/workshops/123e4567-e89b-42d3-a456-999999999999/participants')
        .expect(404);

      expect(response.body).toMatchObject({
        error: expect.stringContaining('not found'),
        code: 'WORKSHOP_NOT_FOUND'
      });
    });

    it('should only return participants for the specified workshop', async () => {
      const otherWorkshop: Workshop = {
        id: '123e4567-e89b-42d3-a456-426614174001', // Valid UUID v4
        title: 'Other Workshop',
        description: 'Another workshop',
        status: 'pending',
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };
      DatabaseService.writeWorkshops([testWorkshop, otherWorkshop]);

      const participants: Participant[] = [
        {
          id: '123e4567-e89b-42d3-a456-111111111111',
          workshop_id: testWorkshop.id,
          user_id: 'user-1',
          signed_up_at: '2024-01-01T00:00:00.000Z'
        },
        {
          id: '123e4567-e89b-42d3-a456-222222222222',
          workshop_id: otherWorkshop.id,
          user_id: 'user-2',
          signed_up_at: '2024-01-01T01:00:00.000Z'
        }
      ];
      DatabaseService.writeParticipants(participants);

      const response = await request(app)
        .get(`/api/workshops/${testWorkshop.id}/participants`)
        .expect(200);

      expect(response.body.participants).toHaveLength(1);
      expect(response.body.participants[0]).toMatchObject({
        user_id: 'user-1',
        workshop_id: testWorkshop.id
      });
    });
  });
});
