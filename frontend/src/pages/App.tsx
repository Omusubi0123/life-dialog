import '../index.css'
import { Datepicker } from "flowbite-react";
import { Accordion } from "flowbite-react";
import { useEffect, useState, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import createDatePickerOption from '../utils/createDatePickerOption.ts';
import Footer from '../components/Footer.tsx';


type MessageItem = {
  media_type: string;
  content: string;
  time: string;
}


export default function App() {
  const [items, setItems] = useState<any>(null);
  const [summary, setSummary] = useState<string>('');
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
        month: month+1,
        day: day,
      };
      const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/diary/fetch_diary`, requestBody);
      setItems(response.data);
      setLoading(false);
      setSummary(response.data.summary);
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
        setSelectedDate(new Date(year, month-1, day));
        post_fetch_diary(userId, year, month, day);
      }
    } else {
      const year = selectedDate.getFullYear();
      const month = selectedDate.getMonth();
      const day = selectedDate.getDate();
      if (userId) {
        post_fetch_diary(userId, year, month, day);
      }
    }
  }, []);

  useEffect(() => {
    const queryParams = new URLSearchParams(window.location.search);
    const userId = queryParams.get("user_id");
    if (userId) {
      post_fetch_diary(userId, selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());
    }
  }, [selectedDate]);

  const handlePreviousDay = () => {
    setSelectedDate(prevDate => {
      const newDate = new Date(prevDate);
      newDate.setDate(prevDate.getDate() - 1);
      return newDate;
    });
  };

  const handleNextDay = () => {
    setSelectedDate(prevDate => {
      const newDate = new Date(prevDate);
      newDate.setDate(prevDate.getDate() + 1);
      return newDate;
    });
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
          <div className="text-gray-500">
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
          <div className="mt-20 mb-5 bg-white space-y-4" id="accordion-open" data-accordion="open">
            <Accordion>
              <Accordion.Panel>
                <Accordion.Title className="bg-gray-200 text-gray-800">この日は何をした日？</Accordion.Title>
                <Accordion.Content>
                  <p className="mb-2 px-4 py-2 text-gray-500 dark:text-gray-400">{summary}</p>
                </Accordion.Content>
              </Accordion.Panel>
            </Accordion>
            <Accordion>
              <Accordion.Panel>
                <Accordion.Title className="bg-gray-200 text-gray-800">AIによる感想</Accordion.Title>
                <Accordion.Content>
                  <p className="mb-2 px-4 py-2 text-gray-500 dark:text-gray-400">{feedback}</p>
                </Accordion.Content>
              </Accordion.Panel>
            </Accordion>
          </div>
          <ol className="relative border-s border-gray-200 dark:border-gray-700">        
            {items.items.map((item: MessageItem, index: number) => (
              <li key={index} className="mb-3 ms-4">
                <div className="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
                  {item.media_type == "text" && "content" in item && "time" in item && (
                    <>
                      <time className="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">{item.time}</time>
                      <p className="mb-2 text-base font-normal text-gray-500 dark:text-gray-400">
                        {item.content}
                      </p>
                    </>
                  )}
                  {item.media_type == "image" && "content" in item && "time" in item && (
                    <>
                      <time className="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">{item.time}</time>
                      <img className="h-auto w-2/3 max-w-full rounded-lg" src={item.content} alt=""></img>
                    </>
                  )}
                  {item.media_type == "video" && "content" in item && "time" in item && (
                    <>
                      <time className="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">{item.time}</time>
                      <video className="h-auto w-2/3 max-w-full rounded-lg" controls>
                        <source src={item.content} type="video/mp4"></source>
                      </video>
                    </>
                  )}
                  {item.media_type == "audio" && "content" in item && "time" in item && (
                    <>
                      <time className="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">{item.time}</time>
                      <audio className="w-2/3 max-w-full" controls>
                        <source src={item.content} type="audio/mp3"></source>
                      </audio>
                    </>
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
