export interface Document {
  id: string;
  title: string;
  type: string;
  path: string;
  created_at: string;
  updated_at: string;
  content?: string | null;
  vector_ids?: string[] | null;
} 