import { useProfileData } from './useProfileData';

export const useProfile = () => {
  const { profile } = useProfileData();

  // 認証済みユーザーのみアクセス可能なため、ルーティング関連は簡略化
  const diaryLink = { pathname: '/', search: '' };
  const profileLink = { pathname: '/profile', search: '' };

  return {
    profile,
    diaryLink,
    profileLink,
  };
};
