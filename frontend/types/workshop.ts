/**
 * Workshop Types
 */

export interface Workshop {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'ongoing' | 'completed';
  signup_enabled: boolean;
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface CreateWorkshopData {
  title: string;
  description: string;
}

export interface UpdateWorkshopData {
  title?: string;
  description?: string;
  status?: 'pending' | 'ongoing' | 'completed';
  signup_enabled?: boolean;
}

export interface Participant {
  id: string;
  workshop_id: string;
  user_id: string;
  status: 'pending' | 'joined' | 'rejected' | 'waitlisted';
  requested_at: string;
  approved_at: string | null;
  approved_by: string | null;
  user_name: string;
  user_email: string;
}

export interface ParticipantWithWorkshop extends Participant {
  workshop_title: string;
  workshop_description: string;
  workshop_status: string;
  workshop_owner_id: string;
}

export interface ParticipantsByStatus {
  pending: Participant[];
  joined: Participant[];
  rejected: Participant[];
  waitlisted: Participant[];
}
