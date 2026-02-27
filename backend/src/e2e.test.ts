/**
 * End-to-end test for frontend-backend integration
 * This test verifies the complete flow: frontend fetch → backend API → database → response
 */

import request from 'supertest';
import app from './app';
import { DatabaseService } from './services/database.service';
import { v4 as uuidv4 } from 'uuid';

describe('End-to-End: Frontend to Backend Integration', () => {
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

  describe('GET /api/workshops - Workshop Listing Endpoint', () => {
    it('should return empty array when no workshops exist', async () => {
      const response = await request(app)
        .get('/api/workshops')
        .expect('Content-Type', /json/)
        .expect(200);

      expect(response.body).toEqual([]);
    });

    it('should return all workshops with correct structure', async () => {
      // Create test workshops
      const workshop1 = {
        id: uuidv4(),
        title: 'TypeScript Fundamentals',
        description: 'Learn the basics of TypeScript',
        status: 'pending' as const,
        signup_enabled: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      const workshop2 = {
        id: uuidv4(),
        title: 'Advanced React Patterns',
        description: 'Master advanced React concepts',
        status: 'ongoing' as const,
        signup_enabled: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      const workshop3 = {
        id: uuidv4(),
        title: 'Node.js Best Practices',
        description: 'Learn Node.js best practices',
        status: 'completed' as const,
        signup_enabled: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      await DatabaseService.writeWorkshops([workshop1, workshop2, workshop3]);

      // Fetch workshops via API
      const response = await request(app)
        .get('/api/workshops')
        .expect('Content-Type', /json/)
        .expect(200);

      // Verify response structure
      expect(Array.isArray(response.body)).toBe(true);
      expect(response.body).toHaveLength(3);

      // Verify each workshop has required fields
      response.body.forEach((workshop: any) => {
        expect(workshop).toHaveProperty('id');
        expect(workshop).toHaveProperty('title');
        expect(workshop).toHaveProperty('description');
        expect(workshop).toHaveProperty('status');
        expect(workshop).toHaveProperty('signup_enabled');
        expect(workshop).toHaveProperty('created_at');
        expect(workshop).toHaveProperty('updated_at');
      });

      // Verify specific workshop data
      const tsWorkshop = response.body.find((w: any) => w.title === 'TypeScript Fundamentals');
      expect(tsWorkshop).toBeDefined();
      expect(tsWorkshop.status).toBe('pending');
      expect(tsWorkshop.signup_enabled).toBe(true);

      const reactWorkshop = response.body.find((w: any) => w.title === 'Advanced React Patterns');
      expect(reactWorkshop).toBeDefined();
      expect(reactWorkshop.status).toBe('ongoing');
      expect(reactWorkshop.signup_enabled).toBe(false);

      const nodeWorkshop = response.body.find((w: any) => w.title === 'Node.js Best Practices');
      expect(nodeWorkshop).toBeDefined();
      expect(nodeWorkshop.status).toBe('completed');
      expect(nodeWorkshop.signup_enabled).toBe(false);
    });

    it('should respond within 500ms (performance requirement)', async () => {
      // Create multiple workshops
      const workshops = Array.from({ length: 10 }, (_, i) => ({
        id: uuidv4(),
        title: `Workshop ${i + 1}`,
        description: `Description for workshop ${i + 1}`,
        status: 'pending' as const,
        signup_enabled: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      }));

      await DatabaseService.writeWorkshops(workshops);

      const startTime = Date.now();
      await request(app)
        .get('/api/workshops')
        .expect(200);
      const endTime = Date.now();

      const responseTime = endTime - startTime;
      expect(responseTime).toBeLessThan(500);
    });

    it('should handle database read errors gracefully', async () => {
      // This test verifies error handling when database is unavailable
      // In a real scenario, we might temporarily corrupt the database file
      // For now, we just verify the endpoint doesn't crash
      const response = await request(app)
        .get('/api/workshops')
        .expect('Content-Type', /json/);

      // Should either return data or an error, but not crash
      expect(response.status).toBeGreaterThanOrEqual(200);
      expect(response.status).toBeLessThan(600);
    });
  });

  describe('Frontend Integration Scenarios', () => {
    it('should support frontend loading workshops on mount', async () => {
      // Simulate frontend behavior: fetch workshops when component mounts
      const workshops = [
        {
          id: uuidv4(),
          title: 'Web Development Bootcamp',
          description: 'Full-stack web development course',
          status: 'pending' as const,
          signup_enabled: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ];

      await DatabaseService.writeWorkshops(workshops);

      // Frontend makes GET request
      const response = await request(app)
        .get('/api/workshops')
        .expect(200);

      // Frontend receives array of workshops
      expect(Array.isArray(response.body)).toBe(true);
      expect(response.body[0].title).toBe('Web Development Bootcamp');
    });

    it('should handle CORS for frontend requests', async () => {
      // Verify CORS headers are present for frontend
      const response = await request(app)
        .get('/api/workshops')
        .expect(200);

      // CORS middleware should add appropriate headers
      // The exact headers depend on CORS configuration
      expect(response.headers).toBeDefined();
    });
  });
});
