import { useState } from 'react';

export const useDateControl = () => {
  // URLパラメータから初期日付を取得
  const getInitialDate = (): Date => {
    const searchParams = new URLSearchParams(window.location.search);
    const dateParam = searchParams.get('date');
    
    if (dateParam && dateParam.length === 8) {
      const year = parseInt(dateParam.substring(0, 4), 10);
      const month = parseInt(dateParam.substring(4, 6), 10) - 1; // 0-indexed
      const day = parseInt(dateParam.substring(6, 8), 10);
      
      // 有効な日付かチェック
      const parsedDate = new Date(year, month, day);
      if (!isNaN(parsedDate.getTime())) {
        return parsedDate;
      }
    }
    
    return new Date(); // デフォルトは今日
  };

  const [selectedDate, setSelectedDate] = useState<Date>(getInitialDate);

  // 日付変更時にURLも更新
  const updateURL = (date: Date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const dateString = `${year}${month}${day}`;
    
    const url = new URL(window.location.href);
    url.searchParams.set('date', dateString);
    window.history.replaceState({}, '', url.toString());
  };

  const handlePreviousDay = () => {
    setSelectedDate((prev) => {
      const newDate = new Date(prev);
      newDate.setDate(prev.getDate() - 1);
      updateURL(newDate);
      return newDate;
    });
  };

  const handleNextDay = () => {
    setSelectedDate((prev) => {
      const newDate = new Date(prev);
      newDate.setDate(prev.getDate() + 1);
      updateURL(newDate);
      return newDate;
    });
  };

  const handleDateChange = (newDate: Date | null) => {
    if (newDate) {
      setSelectedDate(newDate);
      updateURL(newDate);
    }
  };

  return {
    selectedDate,
    handlePreviousDay,
    handleNextDay,
    handleDateChange,
  };
};
