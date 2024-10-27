import '../index.css'
import { Datepicker } from "flowbite-react";
import { Accordion } from "flowbite-react";
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import getTimeFromTimeStamp from '../utils/getTimeFromTimeStamp.ts';
import createDatePickerOption from '../utils/createDatePickerOption.ts';
import Footer from '../components/Footer.tsx';

type TextItem = {
  text: string;
  timestamp: string;
};

type FileItem = {
  url: string;
  timestamp: string;
};

export default function App() {
  const [items, setItems] = useState<any>(null);
  const [feedback, setFeedback] = useState<string>('');
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [loading, setLoading] = useState<boolean>(false);

  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);  
  const diaryLink = {
    pathname: "/",
    search: searchParams.toString(),
  };
  const profileLink = {
    pathname: "/profile",
    search: searchParams.toString(),
  };

  const post_fetch_diary = async (user_id: string, year: number, month: number, day: number) => {
    try {
      setItems([]);
      setLoading(true);
      const requestBody = {
        user_id: user_id,
        year: year,
        month: month,
        day: day,
      };
      const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/diary/fetch_diary`, requestBody);
      setItems(response.data);
      setLoading(false);
      setFeedback(response.data.feedback);
    } catch (err) {
      setItems([]);
    }
  };

  useEffect(() => {
    const queryParams = new URLSearchParams(window.location.search);
    const userId = queryParams.get("user_id");
    const date = queryParams.get("date");
    if (date) {
      const year = parseInt(date.substring(0, 4), 10);
      const month = parseInt(date.substring(4, 6), 10);
      const day = parseInt(date.substring(6, 8), 10);
      if (userId) {
        setSelectedDate(new Date(year, month, day));
        post_fetch_diary(userId, year, month, day);
      }
    } else {
      const year = selectedDate.getFullYear();
      const month = selectedDate.getMonth() + 1;
      const day = selectedDate.getDate();
      if (userId) {
        post_fetch_diary(userId, year, month, day);
      }
    }
  }, []);

   const handlePreviousDay = () => {
    setSelectedDate(prevDate => {
      const newDate = new Date(prevDate);
      newDate.setDate(prevDate.getDate() - 1);
      return newDate;
    });
    const queryParams = new URLSearchParams(window.location.search);
    const userId = queryParams.get("user_id");
    if (userId) {
      post_fetch_diary(userId, selectedDate.getFullYear(), selectedDate.getMonth() + 1, selectedDate.getDate());
    }
  };

  const handleNextDay = () => {
    setSelectedDate(prevDate => {
      const newDate = new Date(prevDate);
      newDate.setDate(prevDate.getDate() + 1);
      return newDate;
    });
    const queryParams = new URLSearchParams(window.location.search);
    const userId = queryParams.get("user_id");
    if (userId) {
      post_fetch_diary(userId, selectedDate.getFullYear(), selectedDate.getMonth() + 1, selectedDate.getDate());
    }
  };

  const handleDateChange = (newDate: Date | null) => {
    if (newDate) {
      setSelectedDate(newDate);
    }
  };

  return (
    <div className="bg-white"> 
      <div className="fixed top-0 left-0 z-50 w-full h-20 bg-white border-t border-gray-200 dark:bg-gray-700 dark:border-gray-600 space-x-4 flex items-center justify-center">
        <button onClick={handlePreviousDay}  className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
          <div className="">
            <Datepicker
              theme={createDatePickerOption()} 
              showClearButton={false} 
              onChange={handleDateChange} 
              value={selectedDate}
            />
          </div>  
        <button onClick={handleNextDay} className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
      {items && Array.isArray(items.items) && items.items.length > 0 ? (
        <div className="mt-24 mb-20 mx-10 bg-white">
            <div className="mt-20 mb-5 bg-white" id="accordion-open" data-accordion="open">
            <Accordion>
              <Accordion.Panel>
                <Accordion.Title className="bg-gray-200 text-gray-800">この日は何をした日？</Accordion.Title>
                <Accordion.Content>
                  <p className="mb-2 px-4 py-2 text-gray-500 dark:text-gray-400">{feedback}</p>
                </Accordion.Content>
              </Accordion.Panel>
            </Accordion>
          </div>
          <ol className="relative border-s border-gray-200 dark:border-gray-700">        
            {items.items.map((item: TextItem | FileItem, index: number) => (
              <li key={index} className="mb-3 ms-4">
                <div className="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
                  {"text" in item && "timestamp" in item && (
                    <>
                      <time className="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">{getTimeFromTimeStamp(item.timestamp)}</time>
                        <p className="mb-2 text-base font-normal text-gray-500 dark:text-gray-400">
                        {item.text}
                      </p>
                    </>
                  )}
                {"url" in item && (
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div>
                      <img className="h-auto max-w-full rounded-lg" src={item.url} alt=""></img>
                    </div>
                  </div>
                )}
              </li>
            ))}
          </ol>
        </div>
      ) : (
        <div className="w-screen">
          <div className="flex items-center justify-center min-h-screen mb-2 text-base font-normal text-gray-500 dark:text-gray-400">
            {loading ? "読み込み中です..." : "この日の記録はまだありません"}
          </div>
        </div>
      )}
      <Footer diaryLink={diaryLink} profileLink={profileLink} />
    </div>
    
  )
}
