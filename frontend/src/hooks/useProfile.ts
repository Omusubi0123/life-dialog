import { useRouting } from './useRouting';
import { useProfileData } from './useProfileData';

export const useProfile = () => {
  const { userId, diaryLink, profileLink } = useRouting();
  const { profile } = useProfileData(userId);

  return {
    profile,
    diaryLink,
    profileLink,
  };
};
