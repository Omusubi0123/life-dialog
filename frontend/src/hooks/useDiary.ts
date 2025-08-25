import { useDateControl } from './useDateControl';
import { useDiaryData } from './useDiaryData';

export const useDiary = () => {
  const { selectedDate, handlePreviousDay, handleNextDay, handleDateChange } = useDateControl();
  const { items, summary, feedback, loading } = useDiaryData(selectedDate);

  // 認証済みユーザーのみアクセス可能なため、ルーティング関連は簡略化
  const diaryLink = { pathname: '/', search: '' };
  const profileLink = { pathname: '/profile', search: '' };

  return {
    items,
    summary,
    feedback,
    selectedDate,
    loading,
    handlePreviousDay,
    handleNextDay,
    handleDateChange,
    diaryLink,
    profileLink,
  };
};
