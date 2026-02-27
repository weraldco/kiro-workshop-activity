import * as fs from 'fs';
import * as path from 'path';
import { DatabaseService } from './database.service';
import { Workshop, Participant, Challenge } from '../types';

const TEST_DB_DIR = path.join(__dirname, '../database');
const WORKSHOPS_FILE = path.join(TEST_DB_DIR, 'workshops.json');
const PARTICIPANTS_FILE = path.join(TEST_DB_DIR, 'participants.json');
const CHALLENGES_FILE = path.join(TEST_DB_DIR, 'challenges.json');

describe('DatabaseService', () => {
  // Backup original files before tests
  let workshopsBackup: string;
  let participantsBackup: string;
  let challengesBackup: string;

  beforeAll(() => {
    // Backup existing data
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
    // Restore original data
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
    // Reset to empty state before each test
    fs.writeFileSync(WORKSHOPS_FILE, JSON.stringify({ workshops: [] }, null, 2));
    fs.writeFileSync(PARTICIPANTS_FILE, JSON.stringify({ participants: [] }, null, 2));
    fs.writeFileSync(CHALLENGES_FILE, JSON.stringify({ challenges: [] }, null, 2));
  });

  describe('Workshop operations', () => {
    it('should read empty workshops array', () => {
      const workshops = DatabaseService.readWorkshops();
      expect(workshops).toEqual([]);
    });

    it('should write and read workshops', () => {
      const testWorkshop: Workshop = {
        id: '123e4567-e89b-42d3-a456-426614174000',
        title: 'Test Workshop',
        description: 'Test Description',
        status: 'pending',
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };

      DatabaseService.writeWorkshops([testWorkshop]);
      const workshops = DatabaseService.readWorkshops();

      expect(workshops).toHaveLength(1);
      expect(workshops[0]).toEqual(testWorkshop);
    });

    it('should perform atomic write for workshops', () => {
      const workshop1: Workshop = {
        id: '123e4567-e89b-42d3-a456-426614174000',
        title: 'Workshop 1',
        description: 'Description 1',
        status: 'pending',
        signup_enabled: true,
        created_at: '2024-01-01T00:00:00.000Z',
        updated_at: '2024-01-01T00:00:00.000Z'
      };

      const workshop2: Workshop = {
        id: '223e4567-e89b-42d3-a456-426614174000',
        title: 'Workshop 2',
        description: 'Description 2',
        status: 'ongoing',
        signup_enabled: false,
        created_at: '2024-01-02T00:00:00.000Z',
        updated_at: '2024-01-02T00:00:00.000Z'
      };

      DatabaseService.writeWorkshops([workshop1]);
      DatabaseService.writeWorkshops([workshop1, workshop2]);

      const workshops = DatabaseService.readWorkshops();
      expect(workshops).toHaveLength(2);
    });
  });

  describe('Participant operations', () => {
    it('should read empty participants array', () => {
      const participants = DatabaseService.readParticipants();
      expect(participants).toEqual([]);
    });

    it('should write and read participants', () => {
      const testParticipant: Participant = {
        id: '323e4567-e89b-42d3-a456-426614174000',
        workshop_id: '123e4567-e89b-42d3-a456-426614174000',
        user_id: 'user123',
        signed_up_at: '2024-01-01T00:00:00.000Z'
      };

      DatabaseService.writeParticipants([testParticipant]);
      const participants = DatabaseService.readParticipants();

      expect(participants).toHaveLength(1);
      expect(participants[0]).toEqual(testParticipant);
    });
  });

  describe('Challenge operations', () => {
    it('should read empty challenges array', () => {
      const challenges = DatabaseService.readChallenges();
      expect(challenges).toEqual([]);
    });

    it('should write and read challenges', () => {
      const testChallenge: Challenge = {
        id: '423e4567-e89b-42d3-a456-426614174000',
        workshop_id: '123e4567-e89b-42d3-a456-426614174000',
        title: 'Test Challenge',
        description: 'Test challenge description',
        html_content: '<p>Challenge content</p>'
      };

      DatabaseService.writeChallenges([testChallenge]);
      const challenges = DatabaseService.readChallenges();

      expect(challenges).toHaveLength(1);
      expect(challenges[0]).toEqual(testChallenge);
    });
  });

  describe('Error handling', () => {
    it('should handle corrupted JSON gracefully', () => {
      fs.writeFileSync(WORKSHOPS_FILE, 'invalid json');
      
      expect(() => DatabaseService.readWorkshops()).toThrow();
    });
  });
});
