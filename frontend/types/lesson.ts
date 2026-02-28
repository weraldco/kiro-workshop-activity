export interface Lesson {
  id: string;
  workshop_id: string;
  title: string;
  description?: string;
  content?: string;
  order_index: number;
  points: number;
  created_at: string;
  updated_at: string;
  materials?: LessonMaterial[];
}

export interface LessonMaterial {
  id: string;
  lesson_id: string;
  material_type: 'video' | 'pdf' | 'link';
  title: string;
  url: string;
  file_size?: number;
  duration?: number;
  created_at: string;
}

export interface CreateLessonData {
  title: string;
  description?: string;
  content?: string;
  order_index?: number;
  points?: number;
}

export interface UpdateLessonData {
  title?: string;
  description?: string;
  content?: string;
  order_index?: number;
  points?: number;
}

export interface CreateMaterialData {
  material_type: 'video' | 'pdf' | 'link';
  title: string;
  url: string;
  file_size?: number;
  duration?: number;
}

export interface LessonCompletionResponse {
  message: string;
  points_earned: number;
  total_points: number;
}
