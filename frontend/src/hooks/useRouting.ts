import { useLocation } from 'react-router-dom';

export const useRouting = () => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const userId = searchParams.get('user_id');

  return {
    userId,
    diaryLink: { pathname: '/', search: searchParams.toString() },
    profileLink: { pathname: '/profile', search: searchParams.toString() },
  };
};
