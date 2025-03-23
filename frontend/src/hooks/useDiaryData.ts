import { useState, useEffect } from 'react';
import axios from 'axios';
import { DiaryResponse } from '../types/diary';

export const useDiaryData = (userId: string | null, selectedDate: Date) => {
  const [items, setItems] = useState<DiaryResponse | null>(null);
  const [summary, setSummary] = useState<string>('');
  const [feedback, setFeedback] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

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
    const searchParams = new URLSearchParams(window.location.search);
    const dateParam = searchParams.get('date');
    if (dateParam && userId) {
      const year = parseInt(dateParam.substring(0, 4), 10);
      const month = parseInt(dateParam.substring(4, 6), 10) - 1;
      const day = parseInt(dateParam.substring(6, 8), 10);
      fetchDiary(year, month, day);
    } else if (userId) {
      fetchDiary(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());
    }
  }, [userId]);

  // 日付変更時の処理
  useEffect(() => {
    if (userId) {
      fetchDiary(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());
    }
  }, [selectedDate, userId]);

  return {
    items,
    summary,
    feedback,
    loading,
  };
};
