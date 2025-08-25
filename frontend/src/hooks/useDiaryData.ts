import { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { DiaryResponse } from '../types/diary';

export const useDiaryData = (selectedDate: Date) => {
  const [items, setItems] = useState<DiaryResponse | null>(null);
  const [summary, setSummary] = useState<string>('');
  const [feedback, setFeedback] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const fetchDiary = async (year: number, month: number, day: number) => {
    const token = Cookies.get('access_token');
    if (!token) return;
    
    try {
      setItems(null);
      setLoading(true);
      const response = await axios.get<DiaryResponse>(
        `${import.meta.env.VITE_BACKEND_URL}/diary/fetch_diary`,
        {
          params: { year, month: month + 1, day },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setItems(response.data);
      setSummary(response.data.summary);
      setFeedback(response.data.feedback);
    } catch (err) {
      setItems(null);
      // 401エラーの場合はログイン画面にリダイレクト
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        Cookies.remove('access_token');
        window.location.href = '/login';
      }
    } finally {
      setLoading(false);
    }
  };

  // 初回ロード時の処理
  useEffect(() => {
    fetchDiary(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());
  }, []);

  // 日付変更時の処理
  useEffect(() => {
    fetchDiary(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());
  }, [selectedDate]);

  return {
    items,
    summary,
    feedback,
    loading,
  };
};
