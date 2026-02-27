import * as fs from 'fs';
import * as path from 'path';
import { ReferentialIntegrityService } from './referential-integrity.service';
import { DatabaseService } from './database.service';
import { Workshop, Participant, Challenge } from '../types';

const TEST_DB_DIR = path.join(__dirname, '../database');
const WORKSHOPS_FILE = path.join(TEST_DB_DIR, 'workshops.json');
const PARTICIPANTS_FILE = path.join(TEST_DB_DIR, 'participants.json');
const CHALLENGES_FILE = path.join(TEST_DB_DIR, 'challenges.json');

describe('ReferentialIntegrityService', () => {
  let workshopsBackup: string;
  let participantsBackup: string;
  let challengesBackup: string;

  beforeAll(() => {
    if (fs.existsSync(WORKSHOPS_FILE)) {
      workshopsBackup = fs.readFileSync(WORKSHOPS_FILE, 'utf-8');
    }
    if (fs.existsSync(PARTICIPANTS_FILE)) {
      participantsBackup = fs.readFileSync(PARTICIPANTS_FILE, 'utf-8');
    }
    if (fs.existsSync(CHALLENGES_FILE)) {
      challengesBackup = fs.readFileSync(CHALLENGES_FILE, 'utf-8');
    }
  });

  afterAll(() => {
    if (workshopsBackup) {
      fs.writeFileSync(WORKSHOPS_FILE, workshopsBackup);
    }
    if (participantsBackup) {
      fs.writeFileSync(PARTICIPANTS_FILE, participantsBackup);
    }
    if (challengesBackup) {
      fs.writeFileSync(CHALLENGES_FILE, challengesBackup);
    }
  });

  beforeEach(() => {
    fs.writeFileSync(WORKSHOPS_FILE, JSON.stringify({ workshops: [] }, null, 2));
    fs.writeFileSync(PARTICIPANTS_FILE, JSON.stringify({ participants: [] }, null, 2));
    fs.writeFileSync(CHALLENGES_FILE, JSON.stringify({ challenges: [] }, null, 2));
  });

  const testWorkshop: Workshop = {
    id: '123e4567-e89b-42d3-a456-426614174000',
    title: 'Test Workshop',
    description: 'Test Description',
    status: 'pending',
    signup_enabled: true,
    created_at: '2024-01-01T00:00:00.000Z',
    updated_at: '2024-01-01T00:00:00.000Z'
  };

  describe('workshopExists', () => {
    it('should return false for non-existent workshop', () => {
      expect(ReferentialIntegrityService.workshopExists('non-existent-id')).toBe(false);
    });

    it('should return true for existing workshop', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      expect(ReferentialIntegrityService.workshopExists(testWorkshop.id)).toBe(true);
    });
  });

  describe('verifyWorkshopExists', () => {
    it('should throw error for non-existent workshop', () => {
      expect(() => ReferentialIntegrityService.verifyWorkshopExists('non-existent-id'))
        .toThrow("Workshop with id 'non-existent-id' does not exist");
    });

    it('should not throw for existing workshop', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      expect(() => ReferentialIntegrityService.verifyWorkshopExists(testWorkshop.id))
        .not.toThrow();
    });
  });

  describe('hasParticipants', () => {
    it('should return false when workshop has no participants', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      expect(ReferentialIntegrityService.hasParticipants(testWorkshop.id)).toBe(false);
    });

    it('should return true when workshop has participants', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      
      const participant: Participant = {
        id: '223e4567-e89b-42d3-a456-426614174000',
        workshop_id: testWorkshop.id,
        user_id: 'user123',
        signed_up_at: '2024-01-01T00:00:00.000Z'
      };
      
      DatabaseService.writeParticipants([participant]);
      expect(ReferentialIntegrityService.hasParticipants(testWorkshop.id)).toBe(true);
    });
  });

  describe('hasChallenges', () => {
    it('should return false when workshop has no challenges', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      expect(ReferentialIntegrityService.hasChallenges(testWorkshop.id)).toBe(false);
    });

    it('should return true when workshop has challenges', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      
      const challenge: Challenge = {
        id: '323e4567-e89b-42d3-a456-426614174000',
        workshop_id: testWorkshop.id,
        title: 'Test Challenge',
        description: 'Test description',
        html_content: '<p>Content</p>'
      };
      
      DatabaseService.writeChallenges([challenge]);
      expect(ReferentialIntegrityService.hasChallenges(testWorkshop.id)).toBe(true);
    });
  });

  describe('checkDependentRecords', () => {
    it('should not throw when workshop has no dependents', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      expect(() => ReferentialIntegrityService.checkDependentRecords(testWorkshop.id))
        .not.toThrow();
    });

    it('should throw when workshop has participants', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      
      const participant: Participant = {
        id: '223e4567-e89b-42d3-a456-426614174000',
        workshop_id: testWorkshop.id,
        user_id: 'user123',
        signed_up_at: '2024-01-01T00:00:00.000Z'
      };
      
      DatabaseService.writeParticipants([participant]);
      
      expect(() => ReferentialIntegrityService.checkDependentRecords(testWorkshop.id))
        .toThrow('has 1 participant(s)');
    });

    it('should throw when workshop has challenges', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      
      const challenge: Challenge = {
        id: '323e4567-e89b-42d3-a456-426614174000',
        workshop_id: testWorkshop.id,
        title: 'Test Challenge',
        description: 'Test description',
        html_content: '<p>Content</p>'
      };
      
      DatabaseService.writeChallenges([challenge]);
      
      expect(() => ReferentialIntegrityService.checkDependentRecords(testWorkshop.id))
        .toThrow('has 1 challenge(s)');
    });

    it('should throw when workshop has both participants and challenges', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      
      const participant: Participant = {
        id: '223e4567-e89b-42d3-a456-426614174000',
        workshop_id: testWorkshop.id,
        user_id: 'user123',
        signed_up_at: '2024-01-01T00:00:00.000Z'
      };
      
      const challenge: Challenge = {
        id: '323e4567-e89b-42d3-a456-426614174000',
        workshop_id: testWorkshop.id,
        title: 'Test Challenge',
        description: 'Test description',
        html_content: '<p>Content</p>'
      };
      
      DatabaseService.writeParticipants([participant]);
      DatabaseService.writeChallenges([challenge]);
      
      expect(() => ReferentialIntegrityService.checkDependentRecords(testWorkshop.id))
        .toThrow('has 1 participant(s) and 1 challenge(s)');
    });
  });

  describe('getWorkshopParticipants', () => {
    it('should return empty array for workshop with no participants', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      expect(ReferentialIntegrityService.getWorkshopParticipants(testWorkshop.id)).toEqual([]);
    });

    it('should return participant IDs for workshop', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      
      const participant1: Participant = {
        id: '223e4567-e89b-42d3-a456-426614174000',
        workshop_id: testWorkshop.id,
        user_id: 'user123',
        signed_up_at: '2024-01-01T00:00:00.000Z'
      };
      
      const participant2: Participant = {
        id: '323e4567-e89b-42d3-a456-426614174000',
        workshop_id: testWorkshop.id,
        user_id: 'user456',
        signed_up_at: '2024-01-02T00:00:00.000Z'
      };
      
      DatabaseService.writeParticipants([participant1, participant2]);
      
      const participantIds = ReferentialIntegrityService.getWorkshopParticipants(testWorkshop.id);
      expect(participantIds).toHaveLength(2);
      expect(participantIds).toContain(participant1.id);
      expect(participantIds).toContain(participant2.id);
    });
  });

  describe('getWorkshopChallenges', () => {
    it('should return empty array for workshop with no challenges', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      expect(ReferentialIntegrityService.getWorkshopChallenges(testWorkshop.id)).toEqual([]);
    });

    it('should return challenge IDs for workshop', () => {
      DatabaseService.writeWorkshops([testWorkshop]);
      
      const challenge1: Challenge = {
        id: '423e4567-e89b-42d3-a456-426614174000',
        workshop_id: testWorkshop.id,
        title: 'Challenge 1',
        description: 'Description 1',
        html_content: '<p>Content 1</p>'
      };
      
      const challenge2: Challenge = {
        id: '523e4567-e89b-42d3-a456-426614174000',
        workshop_id: testWorkshop.id,
        title: 'Challenge 2',
        description: 'Description 2',
        html_content: '<p>Content 2</p>'
      };
      
      DatabaseService.writeChallenges([challenge1, challenge2]);
      
      const challengeIds = ReferentialIntegrityService.getWorkshopChallenges(testWorkshop.id);
      expect(challengeIds).toHaveLength(2);
      expect(challengeIds).toContain(challenge1.id);
      expect(challengeIds).toContain(challenge2.id);
    });
  });
});
