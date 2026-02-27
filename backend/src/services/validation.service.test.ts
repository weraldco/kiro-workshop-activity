import { ValidationService } from './validation.service';
import { Workshop, Participant, Challenge } from '../types';

describe('ValidationService', () => {
  describe('Workshop validation', () => {
    const validWorkshop: Workshop = {
      id: '123e4567-e89b-42d3-a456-426614174000',
      title: 'Valid Workshop',
      description: 'Valid description',
      status: 'pending',
      signup_enabled: true,
      created_at: '2024-01-01T00:00:00.000Z',
      updated_at: '2024-01-01T00:00:00.000Z'
    };

    it('should validate a valid workshop', () => {
      expect(() => ValidationService.validateWorkshop(validWorkshop)).not.toThrow();
    });

    it('should reject workshop with invalid UUID', () => {
      const invalid = { ...validWorkshop, id: 'invalid-uuid' };
      expect(() => ValidationService.validateWorkshop(invalid)).toThrow('must be a valid UUID v4');
    });

    it('should reject workshop with invalid status', () => {
      const invalid = { ...validWorkshop, status: 'invalid' };
      expect(() => ValidationService.validateWorkshop(invalid)).toThrow('must be one of: pending, ongoing, completed');
    });

    it('should reject workshop with title too long', () => {
      const invalid = { ...validWorkshop, title: 'a'.repeat(201) };
      expect(() => ValidationService.validateWorkshop(invalid)).toThrow('title must be between 1 and 200 characters');
    });

    it('should accept workshop with title exactly 200 characters', () => {
      const valid = { ...validWorkshop, title: 'a'.repeat(200) };
      expect(() => ValidationService.validateWorkshop(valid)).not.toThrow();
    });

    it('should reject workshop with empty title', () => {
      const invalid = { ...validWorkshop, title: '' };
      expect(() => ValidationService.validateWorkshop(invalid)).toThrow('title must be between 1 and 200 characters');
    });

    it('should reject workshop with description too long', () => {
      const invalid = { ...validWorkshop, description: 'a'.repeat(1001) };
      expect(() => ValidationService.validateWorkshop(invalid)).toThrow('description must be between 1 and 1000 characters');
    });

    it('should accept workshop with description exactly 1000 characters', () => {
      const valid = { ...validWorkshop, description: 'a'.repeat(1000) };
      expect(() => ValidationService.validateWorkshop(valid)).not.toThrow();
    });

    it('should reject workshop with invalid timestamp', () => {
      const invalid = { ...validWorkshop, created_at: 'invalid-date' };
      expect(() => ValidationService.validateWorkshop(invalid)).toThrow('must be a valid ISO 8601 timestamp');
    });

    it('should reject workshop with non-boolean signup_enabled', () => {
      const invalid = { ...validWorkshop, signup_enabled: 'true' as any };
      expect(() => ValidationService.validateWorkshop(invalid)).toThrow('signup_enabled is required and must be a boolean');
    });

    it('should reject non-object workshop', () => {
      expect(() => ValidationService.validateWorkshop(null)).toThrow('Workshop must be an object');
    });
  });

  describe('Participant validation', () => {
    const validParticipant: Participant = {
      id: '223e4567-e89b-42d3-a456-426614174000',
      workshop_id: '123e4567-e89b-42d3-a456-426614174000',
      user_id: 'user123',
      signed_up_at: '2024-01-01T00:00:00.000Z'
    };

    it('should validate a valid participant', () => {
      expect(() => ValidationService.validateParticipant(validParticipant)).not.toThrow();
    });

    it('should reject participant with invalid id UUID', () => {
      const invalid = { ...validParticipant, id: 'invalid' };
      expect(() => ValidationService.validateParticipant(invalid)).toThrow('id must be a valid UUID v4');
    });

    it('should reject participant with invalid workshop_id UUID', () => {
      const invalid = { ...validParticipant, workshop_id: 'invalid' };
      expect(() => ValidationService.validateParticipant(invalid)).toThrow('workshop_id must be a valid UUID v4');
    });

    it('should reject participant with empty user_id', () => {
      const invalid = { ...validParticipant, user_id: '   ' };
      expect(() => ValidationService.validateParticipant(invalid)).toThrow('user_id cannot be empty');
    });

    it('should reject participant with invalid timestamp', () => {
      const invalid = { ...validParticipant, signed_up_at: 'not-a-date' };
      expect(() => ValidationService.validateParticipant(invalid)).toThrow('must be a valid ISO 8601 timestamp');
    });
  });

  describe('Challenge validation', () => {
    const validChallenge: Challenge = {
      id: '323e4567-e89b-42d3-a456-426614174000',
      workshop_id: '123e4567-e89b-42d3-a456-426614174000',
      title: 'Valid Challenge',
      description: 'Valid challenge description',
      html_content: '<p>Valid HTML content</p>'
    };

    it('should validate a valid challenge', () => {
      expect(() => ValidationService.validateChallenge(validChallenge)).not.toThrow();
    });

    it('should reject challenge with title too long', () => {
      const invalid = { ...validChallenge, title: 'a'.repeat(201) };
      expect(() => ValidationService.validateChallenge(invalid)).toThrow('title must be between 1 and 200 characters');
    });

    it('should accept challenge with title exactly 200 characters', () => {
      const valid = { ...validChallenge, title: 'a'.repeat(200) };
      expect(() => ValidationService.validateChallenge(valid)).not.toThrow();
    });

    it('should reject challenge with description too long', () => {
      const invalid = { ...validChallenge, description: 'a'.repeat(1001) };
      expect(() => ValidationService.validateChallenge(invalid)).toThrow('description must be between 1 and 1000 characters');
    });

    it('should accept challenge with description exactly 1000 characters', () => {
      const valid = { ...validChallenge, description: 'a'.repeat(1000) };
      expect(() => ValidationService.validateChallenge(valid)).not.toThrow();
    });

    it('should accept plain text as HTML', () => {
      const valid = { ...validChallenge, html_content: 'Plain text content' };
      expect(() => ValidationService.validateChallenge(valid)).not.toThrow();
    });

    it('should accept valid HTML with matching tags', () => {
      const valid = { ...validChallenge, html_content: '<div><p>Content</p></div>' };
      expect(() => ValidationService.validateChallenge(valid)).not.toThrow();
    });

    it('should reject empty HTML content', () => {
      const invalid = { ...validChallenge, html_content: '' };
      expect(() => ValidationService.validateChallenge(invalid)).toThrow('html_content must be valid HTML');
    });

    it('should accept self-closing tags', () => {
      const valid = { ...validChallenge, html_content: '<br/><img src="test.jpg"/>' };
      expect(() => ValidationService.validateChallenge(valid)).not.toThrow();
    });
  });
});
