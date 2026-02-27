import { DatabaseService } from './database.service';

/**
 * Referential Integrity Service for maintaining data consistency
 */
export class ReferentialIntegrityService {
  /**
   * Verify that a workshop exists
   * @param workshopId The workshop ID to check
   * @returns true if workshop exists, false otherwise
   */
  static workshopExists(workshopId: string): boolean {
    const workshops = DatabaseService.readWorkshops();
    return workshops.some(w => w.id === workshopId);
  }

  /**
   * Verify that a workshop exists before creating a participant or challenge
   * @param workshopId The workshop ID to verify
   * @throws Error if workshop does not exist
   */
  static verifyWorkshopExists(workshopId: string): void {
    if (!this.workshopExists(workshopId)) {
      throw new Error(`Workshop with id '${workshopId}' does not exist`);
    }
  }

  /**
   * Check if a workshop has any participants
   * @param workshopId The workshop ID to check
   * @returns true if workshop has participants, false otherwise
   */
  static hasParticipants(workshopId: string): boolean {
    const participants = DatabaseService.readParticipants();
    return participants.some(p => p.workshop_id === workshopId);
  }

  /**
   * Check if a workshop has any challenges
   * @param workshopId The workshop ID to check
   * @returns true if workshop has challenges, false otherwise
   */
  static hasChallenges(workshopId: string): boolean {
    const challenges = DatabaseService.readChallenges();
    return challenges.some(c => c.workshop_id === workshopId);
  }

  /**
   * Check for dependent records before deleting a workshop
   * @param workshopId The workshop ID to check
   * @throws Error if workshop has dependent participants or challenges
   */
  static checkDependentRecords(workshopId: string): void {
    const hasParticipants = this.hasParticipants(workshopId);
    const hasChallenges = this.hasChallenges(workshopId);

    if (hasParticipants && hasChallenges) {
      throw new Error(
        `Cannot delete workshop '${workshopId}': has ${this.getParticipantCount(workshopId)} participant(s) and ${this.getChallengeCount(workshopId)} challenge(s)`
      );
    } else if (hasParticipants) {
      throw new Error(
        `Cannot delete workshop '${workshopId}': has ${this.getParticipantCount(workshopId)} participant(s)`
      );
    } else if (hasChallenges) {
      throw new Error(
        `Cannot delete workshop '${workshopId}': has ${this.getChallengeCount(workshopId)} challenge(s)`
      );
    }
  }

  /**
   * Get the count of participants for a workshop
   * @param workshopId The workshop ID
   * @returns Number of participants
   */
  private static getParticipantCount(workshopId: string): number {
    const participants = DatabaseService.readParticipants();
    return participants.filter(p => p.workshop_id === workshopId).length;
  }

  /**
   * Get the count of challenges for a workshop
   * @param workshopId The workshop ID
   * @returns Number of challenges
   */
  private static getChallengeCount(workshopId: string): number {
    const challenges = DatabaseService.readChallenges();
    return challenges.filter(c => c.workshop_id === workshopId).length;
  }

  /**
   * Get all participants for a workshop
   * @param workshopId The workshop ID
   * @returns Array of participant IDs
   */
  static getWorkshopParticipants(workshopId: string): string[] {
    const participants = DatabaseService.readParticipants();
    return participants
      .filter(p => p.workshop_id === workshopId)
      .map(p => p.id);
  }

  /**
   * Get all challenges for a workshop
   * @param workshopId The workshop ID
   * @returns Array of challenge IDs
   */
  static getWorkshopChallenges(workshopId: string): string[] {
    const challenges = DatabaseService.readChallenges();
    return challenges
      .filter(c => c.workshop_id === workshopId)
      .map(c => c.id);
  }
}
