import { Workshop } from '../types';
import { DatabaseService } from './database.service';

/**
 * Access Control Service for authorization logic
 */
export class AccessControlService {
  /**
   * Check if signup is allowed for a workshop
   * Requirements: 1.3, 2.1, 2.3, 2.4, 6.2, 6.3
   * 
   * @param workshop Workshop to check
   * @returns true if signup is allowed, false otherwise
   */
  static canSignup(workshop: Workshop): boolean {
    // Requirement 6.2: When Signup_Flag is false, reject all signups
    if (!workshop.signup_enabled) {
      return false;
    }

    // Requirements 2.1, 6.3: Accept signups when status is pending and signup_enabled is true
    // Requirements 2.3, 2.4: Reject signups when status is ongoing or completed
    return workshop.status === 'pending';
  }

  /**
   * Check if a user can access challenges for a workshop
   * Requirements: 3.1, 3.2, 3.3, 3.4
   * 
   * @param workshop Workshop to check
   * @param userId User ID to check
   * @returns true if user can access challenges, false otherwise
   */
  static canAccessChallenges(workshop: Workshop, userId: string): boolean {
    // Requirements 3.2, 3.3: Deny access when status is pending or completed
    if (workshop.status !== 'ongoing') {
      return false;
    }

    // Requirement 3.1: Provide access to signed-up participants when status is ongoing
    // Requirement 3.4: Return authorization error for non-signed-up participants
    return this.isParticipant(workshop.id, userId);
  }

  /**
   * Check if a user is a participant in a workshop
   * 
   * @param workshopId Workshop ID to check
   * @param userId User ID to check
   * @returns true if user is a participant, false otherwise
   */
  static isParticipant(workshopId: string, userId: string): boolean {
    const participants = DatabaseService.readParticipants();
    return participants.some(
      p => p.workshop_id === workshopId && p.user_id === userId
    );
  }
}
