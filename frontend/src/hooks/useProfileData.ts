import { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import parseDateString from '../utils/parseDateString';
import { ProfileData, ProfileResponse } from '../types/profile';

export const useProfileData = () => {
  const [profile, setProfile] = useState<ProfileData>({
    name: null,
    iconUrl: null,
    personality: null,
    strength: null,
    weakness: null,
    createdAt: null,
    updatedAt: null,
  });

  const fetchProfile = async () => {
    const token = Cookies.get('access_token');
    if (!token) return;

    try {
      const response = await axios.get<ProfileResponse>(
        `${import.meta.env.VITE_BACKEND_URL}/user/fetch_profile`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setProfile({
        name: response.data.name,
        iconUrl: response.data.icon_url,
        personality: response.data.personality,
        strength: response.data.strength,
        weakness: response.data.weakness,
        createdAt: parseDateString(response.data.created_at),
        updatedAt: parseDateString(new Date().toISOString()),
      });
    } catch (err) {
      console.error('Failed to fetch profile:', err);
      // 401エラーの場合はログイン画面にリダイレクト
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        Cookies.remove('access_token');
        window.location.href = '/login';
      }
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  return { profile };
};
