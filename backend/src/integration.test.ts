import request from 'supertest';
import app from './app';
import { DatabaseService } from './services/database.service';

/**
 * Integration test to verify all API endpoints are accessible
 * Tests task 11.1: Wire all backend components together
 */
describe('API Integration - All Endpoints Accessible', () => {
  beforeEach(() => {
    // Clear database before each test
    DatabaseService.writeWorkshops([]);
    DatabaseService.writeParticipants([]);
    DatabaseService.writeChallenges([]);
  });

  afterAll(() => {
    // Clean up after all tests
    DatabaseService.writeWorkshops([]);
    DatabaseService.writeParticipants([]);
    DatabaseService.writeChallenges([]);
  });

  describe('Workshop Endpoints', () => {
    it('POST /api/workshops should be accessible', async () => {
      const response = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'Test Description'
        });
      
      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('id');
    });

    it('GET /api/workshops should be accessible', async () => {
      const response = await request(app).get('/api/workshops');
      
      expect(response.status).toBe(200);
      expect(Array.isArray(response.body)).toBe(true);
    });

    it('PATCH /api/workshops/:id/status should be accessible', async () => {
      // Create a workshop first
      const createResponse = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'Test Description'
        });
      
      const workshopId = createResponse.body.id;

      const response = await request(app)
        .patch(`/api/workshops/${workshopId}/status`)
        .send({ status: 'ongoing' });
      
      expect(response.status).toBe(200);
      expect(response.body.status).toBe('ongoing');
    });

    it('PATCH /api/workshops/:id/signup-flag should be accessible', async () => {
      // Create a workshop first
      const createResponse = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'Test Description'
        });
      
      const workshopId = createResponse.body.id;

      const response = await request(app)
        .patch(`/api/workshops/${workshopId}/signup-flag`)
        .send({ signup_enabled: false });
      
      expect(response.status).toBe(200);
      expect(response.body.signup_enabled).toBe(false);
    });
  });

  describe('Participant Endpoints', () => {
    it('POST /api/workshops/:id/signup should be accessible', async () => {
      // Create a workshop first
      const createResponse = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'Test Description'
        });
      
      const workshopId = createResponse.body.id;

      const response = await request(app)
        .post(`/api/workshops/${workshopId}/signup`)
        .send({ user_id: 'user123' });
      
      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
    });

    it('GET /api/workshops/:id/participants should be accessible', async () => {
      // Create a workshop first
      const createResponse = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'Test Description'
        });
      
      const workshopId = createResponse.body.id;

      const response = await request(app)
        .get(`/api/workshops/${workshopId}/participants`);
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('participants');
    });
  });

  describe('Challenge Endpoints', () => {
    it('POST /api/workshops/:id/challenges should be accessible', async () => {
      // Create a workshop first
      const createResponse = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'Test Description'
        });
      
      const workshopId = createResponse.body.id;

      const response = await request(app)
        .post(`/api/workshops/${workshopId}/challenges`)
        .send({
          title: 'Test Challenge',
          description: 'Test Challenge Description',
          html_content: '<p>Test HTML</p>'
        });
      
      expect(response.status).toBe(201);
      expect(response.body.success).toBe(true);
      expect(response.body).toHaveProperty('challenge_id');
    });

    it('GET /api/workshops/:id/challenges should be accessible', async () => {
      // Create a workshop and sign up a participant
      const createResponse = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'Test Description'
        });
      
      const workshopId = createResponse.body.id;

      // Sign up participant
      await request(app)
        .post(`/api/workshops/${workshopId}/signup`)
        .send({ user_id: 'user123' });

      // Change status to ongoing
      await request(app)
        .patch(`/api/workshops/${workshopId}/status`)
        .send({ status: 'ongoing' });

      const response = await request(app)
        .get(`/api/workshops/${workshopId}/challenges?user_id=user123`);
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('challenges');
    });

    it('GET /api/challenges/:id should be accessible', async () => {
      // Create a workshop, challenge, and sign up a participant
      const createResponse = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'Test Description'
        });
      
      const workshopId = createResponse.body.id;

      // Create challenge
      const challengeResponse = await request(app)
        .post(`/api/workshops/${workshopId}/challenges`)
        .send({
          title: 'Test Challenge',
          description: 'Test Challenge Description',
          html_content: '<p>Test HTML</p>'
        });
      
      const challengeId = challengeResponse.body.challenge_id;

      // Sign up participant
      await request(app)
        .post(`/api/workshops/${workshopId}/signup`)
        .send({ user_id: 'user123' });

      // Change status to ongoing
      await request(app)
        .patch(`/api/workshops/${workshopId}/status`)
        .send({ status: 'ongoing' });

      const response = await request(app)
        .get(`/api/challenges/${challengeId}?user_id=user123`);
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('challenge');
    });
  });

  describe('Error Handling and Middleware', () => {
    it('should return 404 for non-existent endpoints', async () => {
      const response = await request(app).get('/api/nonexistent');
      
      expect(response.status).toBe(404);
      expect(response.body).toHaveProperty('error');
      expect(response.body.code).toBe('NOT_FOUND');
    });

    it('should have CORS enabled', async () => {
      const response = await request(app)
        .get('/api/workshops')
        .set('Origin', 'http://localhost:3000');
      
      expect(response.headers['access-control-allow-origin']).toBeDefined();
    });

    it('should parse JSON request bodies', async () => {
      const response = await request(app)
        .post('/api/workshops')
        .send({
          title: 'Test Workshop',
          description: 'Test Description'
        })
        .set('Content-Type', 'application/json');
      
      expect(response.status).toBe(201);
    });

    it('health check endpoint should be accessible', async () => {
      const response = await request(app).get('/health');
      
      expect(response.status).toBe(200);
      expect(response.body.status).toBe('ok');
      expect(response.body).toHaveProperty('timestamp');
    });
  });
});
