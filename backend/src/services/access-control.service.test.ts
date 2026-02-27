import { AccessControlService } from './access-control.service';
import { DatabaseService } from './database.service';
import { Workshop, Participant } from '../types';

// Mock DatabaseService
jest.mock('./database.service');

describe('AccessControlService', () => {
  describe('canSignup', () => {
    it('should allow signup when status is pending and signup_enabled is true', () => {
      const workshop: Workshop = {
        id: 'workshop-1',
        title: 'Test Workshop',
        description: 'Test Description',
        status: 'pending',
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };

      expect(AccessControlService.canSignup(workshop)).toBe(true);
    });

    it('should reject signup when signup_enabled is false', () => {
      const workshop: Workshop = {
        id: 'workshop-1',
        title: 'Test Workshop',
        description: 'Test Description',
        status: 'pending',
        signup_enabled: false,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };

      expect(AccessControlService.canSignup(workshop)).toBe(false);
    });

    it('should reject signup when status is ongoing', () => {
      const workshop: Workshop = {
        id: 'workshop-1',
        title: 'Test Workshop',
        description: 'Test Description',
        status: 'ongoing',
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };

      expect(AccessControlService.canSignup(workshop)).toBe(false);
    });

    it('should reject signup when status is completed', () => {
      const workshop: Workshop = {
        id: 'workshop-1',
        title: 'Test Workshop',
        description: 'Test Description',
        status: 'completed',
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };

      expect(AccessControlService.canSignup(workshop)).toBe(false);
    });
  });

  describe('isParticipant', () => {
    beforeEach(() => {
      jest.clearAllMocks();
    });

    it('should return true when user is a participant', () => {
      const participants: Participant[] = [
        {
          id: 'participant-1',
          workshop_id: 'workshop-1',
          user_id: 'user-1',
          signed_up_at: '2024-01-01T00:00:00.000Z'
        }
      ];

      (DatabaseService.readParticipants as jest.Mock).mockReturnValue(participants);

      expect(AccessControlService.isParticipant('workshop-1', 'user-1')).toBe(true);
    });

    it('should return false when user is not a participant', () => {
      const participants: Participant[] = [
        {
          id: 'participant-1',
          workshop_id: 'workshop-1',
          user_id: 'user-1',
          signed_up_at: '2024-01-01T00:00:00.000Z'
        }
      ];

      (DatabaseService.readParticipants as jest.Mock).mockReturnValue(participants);

      expect(AccessControlService.isParticipant('workshop-1', 'user-2')).toBe(false);
    });

    it('should return false when workshop has no participants', () => {
      (DatabaseService.readParticipants as jest.Mock).mockReturnValue([]);

      expect(AccessControlService.isParticipant('workshop-1', 'user-1')).toBe(false);
    });
  });

  describe('canAccessChallenges', () => {
    beforeEach(() => {
      jest.clearAllMocks();
    });

    it('should allow access when status is ongoing and user is participant', () => {
      const workshop: Workshop = {
        id: 'workshop-1',
        title: 'Test Workshop',
        description: 'Test Description',
        status: 'ongoing',
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };

      const participants: Participant[] = [
        {
          id: 'participant-1',
          workshop_id: 'workshop-1',
          user_id: 'user-1',
          signed_up_at: '2024-01-01T00:00:00.000Z'
        }
      ];

      (DatabaseService.readParticipants as jest.Mock).mockReturnValue(participants);

      expect(AccessControlService.canAccessChallenges(workshop, 'user-1')).toBe(true);
    });

    it('should deny access when status is pending', () => {
      const workshop: Workshop = {
        id: 'workshop-1',
        title: 'Test Workshop',
        description: 'Test Description',
        status: 'pending',
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };

      expect(AccessControlService.canAccessChallenges(workshop, 'user-1')).toBe(false);
    });

    it('should deny access when status is completed', () => {
      const workshop: Workshop = {
        id: 'workshop-1',
        title: 'Test Workshop',
        description: 'Test Description',
        status: 'completed',
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };

      expect(AccessControlService.canAccessChallenges(workshop, 'user-1')).toBe(false);
    });

    it('should deny access when user is not a participant', () => {
      const workshop: Workshop = {
        id: 'workshop-1',
        title: 'Test Workshop',
        description: 'Test Description',
        status: 'ongoing',
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };

      (DatabaseService.readParticipants as jest.Mock).mockReturnValue([]);

      expect(AccessControlService.canAccessChallenges(workshop, 'user-1')).toBe(false);
    });
  });
});
