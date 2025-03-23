import { useRouting } from './useRouting';
import { useDateControl } from './useDateControl';
import { useDiaryData } from './useDiaryData';

export const useDiary = () => {
  const { userId, diaryLink, profileLink } = useRouting();
  const { selectedDate, handlePreviousDay, handleNextDay, handleDateChange } = useDateControl();
  const { items, summary, feedback, loading } = useDiaryData(userId, selectedDate);

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
