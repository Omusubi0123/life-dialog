import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import parseDateString from '../utils/parseDateString';
import { ProfileData, ProfileResponse } from '../types/profile';

export const useProfile = () => {
  const [profile, setProfile] = useState<ProfileData>({
    name: null,
    iconUrl: null,
    personality: null,
    strength: null,
    weakness: null,
    createdAt: null,
    updatedAt: null,
  });

  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const userId = searchParams.get('user_id');

  const fetchProfile = async (userId: string) => {
    try {
      const response = await axios.post<ProfileResponse>(
        `${import.meta.env.VITE_BACKEND_URL}/user/fetch_profile`,
        { user_id: userId }
      );
      setProfile({
        name: response.data.name,
        iconUrl: response.data.icon_url,
        personality: response.data.personality,
        strength: response.data.strength,
        weakness: response.data.weakness,
        createdAt: parseDateString(response.data.created_at),
        updatedAt: parseDateString(new Date().toISOString()), // updated_at がサーバーから返されない場合を考慮
      });
    } catch (err) {
      console.error('Failed to fetch profile:', err);
    }
  };

  useEffect(() => {
    if (userId) {
      fetchProfile(userId);
    }
  }, []);

  return {
    profile,
    diaryLink: { pathname: '/', search: searchParams.toString() },
    profileLink: { pathname: '/profile', search: searchParams.toString() },
  };
};
