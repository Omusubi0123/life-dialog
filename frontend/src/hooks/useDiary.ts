import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { DiaryResponse } from '../types/diary';

export const useDiary = () => {
  const [items, setItems] = useState<DiaryResponse | null>(null);
  const [summary, setSummary] = useState<string>('');
  const [feedback, setFeedback] = useState<string>('');
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [loading, setLoading] = useState<boolean>(false);

  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const userId = searchParams.get('user_id');

  const fetchDiary = async (year: number, month: number, day: number) => {
    if (!userId) return;
    try {
      setItems(null);
      setLoading(true);
      const response = await axios.post<DiaryResponse>(
        `${import.meta.env.VITE_BACKEND_URL}/diary/fetch_diary`,
        { user_id: userId, year, month: month + 1, day }
      );
      setItems(response.data);
      setSummary(response.data.summary);
      setFeedback(response.data.feedback);
    } catch (err) {
      setItems(null);
    } finally {
      setLoading(false);
    }
  };

  // 初回ロード時の処理
  useEffect(() => {
    const dateParam = searchParams.get('date');
    if (dateParam && userId) {
      const year = parseInt(dateParam.substring(0, 4), 10);
      const month = parseInt(dateParam.substring(4, 6), 10) - 1;
      const day = parseInt(dateParam.substring(6, 8), 10);
      setSelectedDate(new Date(year, month, day));
      fetchDiary(year, month, day);
    } else if (userId) {
      fetchDiary(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());
    }
  }, []);

  // 日付変更時の処理
  useEffect(() => {
    if (userId) {
      fetchDiary(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());
    }
  }, [selectedDate]);

  const handlePreviousDay = () => {
    setSelectedDate((prev) => {
      const newDate = new Date(prev);
      newDate.setDate(prev.getDate() - 1);
      return newDate;
    });
  };

  const handleNextDay = () => {
    setSelectedDate((prev) => {
      const newDate = new Date(prev);
      newDate.setDate(prev.getDate() + 1);
      return newDate;
    });
  };

  const handleDateChange = (newDate: Date | null) => {
    if (newDate) setSelectedDate(newDate);
  };

  return {
    items,
    summary,
    feedback,
    selectedDate,
    loading,
    handlePreviousDay,
    handleNextDay,
    handleDateChange,
    diaryLink: { pathname: '/', search: searchParams.toString() },
    profileLink: { pathname: '/profile', search: searchParams.toString() },
  };
};
