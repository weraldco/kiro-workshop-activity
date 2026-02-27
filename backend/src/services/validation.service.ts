import { Workshop, Participant, Challenge } from '../types';

/**
 * Validation Service for schema validation
 */
export class ValidationService {
  /**
   * Validate UUID v4 format
   */
  private static isValidUUID(uuid: string): boolean {
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    return uuidRegex.test(uuid);
  }

  /**
   * Validate ISO 8601 timestamp format
   */
  private static isValidISO8601(timestamp: string): boolean {
    const date = new Date(timestamp);
    return !isNaN(date.getTime()) && date.toISOString() === timestamp;
  }

  /**
   * Validate workshop status enum
   */
  private static isValidStatus(status: string): status is 'pending' | 'ongoing' | 'completed' {
    return status === 'pending' || status === 'ongoing' || status === 'completed';
  }

  /**
   * Basic HTML validation - checks for matching tags
   */
  private static isValidHTML(html: string): boolean {
    if (!html || html.trim().length === 0) {
      return false;
    }

    // Basic check: count opening and closing tags
    const openTags = html.match(/<[^/][^>]*>/g) || [];
    const closeTags = html.match(/<\/[^>]+>/g) || [];
    
    // Self-closing tags like <br/>, <img/>, etc.
    const selfClosingTags = html.match(/<[^>]+\/>/g) || [];
    
    // For basic validation, we'll accept if:
    // 1. It's a plain text (no tags)
    // 2. Opening tags + self-closing tags >= closing tags (allowing for void elements like <br>, <img>)
    const hasNoTags = openTags.length === 0 && closeTags.length === 0;
    const tagsBalanced = openTags.length + selfClosingTags.length >= closeTags.length;
    
    return hasNoTags || tagsBalanced;
  }

  /**
   * Validate Workshop schema
   * @throws Error with descriptive message if validation fails
   */
  static validateWorkshop(workshop: any): asserts workshop is Workshop {
    // Check all required fields exist
    if (!workshop || typeof workshop !== 'object') {
      throw new Error('Workshop must be an object');
    }

    if (!workshop.id || typeof workshop.id !== 'string') {
      throw new Error('Workshop id is required and must be a string');
    }

    if (!this.isValidUUID(workshop.id)) {
      throw new Error('Workshop id must be a valid UUID v4');
    }

    if (typeof workshop.title !== 'string') {
      throw new Error('Workshop title is required and must be a string');
    }

    if (workshop.title.trim().length === 0 || workshop.title.length > 200) {
      throw new Error('Workshop title must be between 1 and 200 characters');
    }

    if (!workshop.description || typeof workshop.description !== 'string') {
      throw new Error('Workshop description is required and must be a string');
    }

    if (workshop.description.length === 0 || workshop.description.length > 1000) {
      throw new Error('Workshop description must be between 1 and 1000 characters');
    }

    if (!workshop.status || typeof workshop.status !== 'string') {
      throw new Error('Workshop status is required and must be a string');
    }

    if (!this.isValidStatus(workshop.status)) {
      throw new Error('Workshop status must be one of: pending, ongoing, completed');
    }

    if (typeof workshop.signup_enabled !== 'boolean') {
      throw new Error('Workshop signup_enabled is required and must be a boolean');
    }

    if (!workshop.created_at || typeof workshop.created_at !== 'string') {
      throw new Error('Workshop created_at is required and must be a string');
    }

    if (!this.isValidISO8601(workshop.created_at)) {
      throw new Error('Workshop created_at must be a valid ISO 8601 timestamp');
    }

    if (!workshop.updated_at || typeof workshop.updated_at !== 'string') {
      throw new Error('Workshop updated_at is required and must be a string');
    }

    if (!this.isValidISO8601(workshop.updated_at)) {
      throw new Error('Workshop updated_at must be a valid ISO 8601 timestamp');
    }
  }

  /**
   * Validate Participant schema
   * @throws Error with descriptive message if validation fails
   */
  static validateParticipant(participant: any): asserts participant is Participant {
    if (!participant || typeof participant !== 'object') {
      throw new Error('Participant must be an object');
    }

    if (!participant.id || typeof participant.id !== 'string') {
      throw new Error('Participant id is required and must be a string');
    }

    if (!this.isValidUUID(participant.id)) {
      throw new Error('Participant id must be a valid UUID v4');
    }

    if (!participant.workshop_id || typeof participant.workshop_id !== 'string') {
      throw new Error('Participant workshop_id is required and must be a string');
    }

    if (!this.isValidUUID(participant.workshop_id)) {
      throw new Error('Participant workshop_id must be a valid UUID v4');
    }

    if (!participant.user_id || typeof participant.user_id !== 'string') {
      throw new Error('Participant user_id is required and must be a string');
    }

    if (participant.user_id.trim().length === 0) {
      throw new Error('Participant user_id cannot be empty');
    }

    if (!participant.signed_up_at || typeof participant.signed_up_at !== 'string') {
      throw new Error('Participant signed_up_at is required and must be a string');
    }

    if (!this.isValidISO8601(participant.signed_up_at)) {
      throw new Error('Participant signed_up_at must be a valid ISO 8601 timestamp');
    }
  }

  /**
   * Validate Challenge schema
   * @throws Error with descriptive message if validation fails
   */
  static validateChallenge(challenge: any): asserts challenge is Challenge {
    if (!challenge || typeof challenge !== 'object') {
      throw new Error('Challenge must be an object');
    }

    if (!challenge.id || typeof challenge.id !== 'string') {
      throw new Error('Challenge id is required and must be a string');
    }

    if (!this.isValidUUID(challenge.id)) {
      throw new Error('Challenge id must be a valid UUID v4');
    }

    if (!challenge.workshop_id || typeof challenge.workshop_id !== 'string') {
      throw new Error('Challenge workshop_id is required and must be a string');
    }

    if (!this.isValidUUID(challenge.workshop_id)) {
      throw new Error('Challenge workshop_id must be a valid UUID v4');
    }

    if (!challenge.title || typeof challenge.title !== 'string') {
      throw new Error('Challenge title is required and must be a string');
    }

    if (challenge.title.length === 0 || challenge.title.length > 200) {
      throw new Error('Challenge title must be between 1 and 200 characters');
    }

    if (!challenge.description || typeof challenge.description !== 'string') {
      throw new Error('Challenge description is required and must be a string');
    }

    if (challenge.description.length === 0 || challenge.description.length > 1000) {
      throw new Error('Challenge description must be between 1 and 1000 characters');
    }

    if (typeof challenge.html_content !== 'string') {
      throw new Error('Challenge html_content is required and must be a string');
    }

    if (challenge.html_content.trim().length === 0) {
      throw new Error('Challenge html_content must be valid HTML');
    }

    if (!this.isValidHTML(challenge.html_content)) {
      throw new Error('Challenge html_content must be valid HTML');
    }
  }
}
