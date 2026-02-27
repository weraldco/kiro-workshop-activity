import * as fs from 'fs';
import * as path from 'path';
import { Workshop, Participant, Challenge } from '../types';

const DB_DIR = path.join(__dirname, '../database');
const WORKSHOPS_FILE = path.join(DB_DIR, 'workshops.json');
const PARTICIPANTS_FILE = path.join(DB_DIR, 'participants.json');
const CHALLENGES_FILE = path.join(DB_DIR, 'challenges.json');

// Ensure database directory exists
if (!fs.existsSync(DB_DIR)) {
  fs.mkdirSync(DB_DIR, { recursive: true });
}

interface WorkshopsData {
  workshops: Workshop[];
}

interface ParticipantsData {
  participants: Participant[];
}

interface ChallengesData {
  challenges: Challenge[];
}

/**
 * Database Service for atomic read/write operations on JSON files
 */
export class DatabaseService {
  /**
   * Read all workshops from the database
   * @throws Error if file read fails or JSON is invalid
   */
  static readWorkshops(): Workshop[] {
    try {
      const data = fs.readFileSync(WORKSHOPS_FILE, 'utf-8');
      const parsed: WorkshopsData = JSON.parse(data);
      return parsed.workshops || [];
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        // File doesn't exist, return empty array
        return [];
      }
      throw new Error(`Failed to read workshops: ${(error as Error).message}`);
    }
  }

  /**
   * Write workshops to the database atomically
   * @param workshops Array of workshops to persist
   * @throws Error if file write fails
   */
  static writeWorkshops(workshops: Workshop[]): void {
    try {
      const data: WorkshopsData = { workshops };
      const jsonString = JSON.stringify(data, null, 2);
      
      // Atomic write: write to temp file, then rename
      const tempFile = `${WORKSHOPS_FILE}.tmp`;
      fs.writeFileSync(tempFile, jsonString, 'utf-8');
      fs.renameSync(tempFile, WORKSHOPS_FILE);
    } catch (error) {
      throw new Error(`Failed to write workshops: ${(error as Error).message}`);
    }
  }

  /**
   * Read all participants from the database
   * @throws Error if file read fails or JSON is invalid
   */
  static readParticipants(): Participant[] {
    try {
      const data = fs.readFileSync(PARTICIPANTS_FILE, 'utf-8');
      const parsed: ParticipantsData = JSON.parse(data);
      return parsed.participants || [];
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        return [];
      }
      throw new Error(`Failed to read participants: ${(error as Error).message}`);
    }
  }

  /**
   * Write participants to the database atomically
   * @param participants Array of participants to persist
   * @throws Error if file write fails
   */
  static writeParticipants(participants: Participant[]): void {
    try {
      const data: ParticipantsData = { participants };
      const jsonString = JSON.stringify(data, null, 2);
      
      const tempFile = `${PARTICIPANTS_FILE}.tmp`;
      fs.writeFileSync(tempFile, jsonString, 'utf-8');
      fs.renameSync(tempFile, PARTICIPANTS_FILE);
    } catch (error) {
      throw new Error(`Failed to write participants: ${(error as Error).message}`);
    }
  }

  /**
   * Read all challenges from the database
   * @throws Error if file read fails or JSON is invalid
   */
  static readChallenges(): Challenge[] {
    try {
      const data = fs.readFileSync(CHALLENGES_FILE, 'utf-8');
      const parsed: ChallengesData = JSON.parse(data);
      return parsed.challenges || [];
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        return [];
      }
      throw new Error(`Failed to read challenges: ${(error as Error).message}`);
    }
  }

  /**
   * Write challenges to the database atomically
   * @param challenges Array of challenges to persist
   * @throws Error if file write fails
   */
  static writeChallenges(challenges: Challenge[]): void {
    try {
      const data: ChallengesData = { challenges };
      const jsonString = JSON.stringify(data, null, 2);
      
      const tempFile = `${CHALLENGES_FILE}.tmp`;
      fs.writeFileSync(tempFile, jsonString, 'utf-8');
      fs.renameSync(tempFile, CHALLENGES_FILE);
    } catch (error) {
      throw new Error(`Failed to write challenges: ${(error as Error).message}`);
    }
  }
}
