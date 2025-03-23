export type ProfileResponse = {
    name: string;
    icon_url: string;
    personality: string;
    strength: string;
    weakness: string;
    created_at: string;
    updated_at: string;
  };
  
  export type ProfileData = {
    name: string | null;
    iconUrl: string | null;
    personality: string | null;
    strength: string | null;
    weakness: string | null;
    createdAt: string | null;
    updatedAt: string | null;
  };
