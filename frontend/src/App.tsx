import './index.css'
import { Datepicker } from "flowbite-react";
import { Accordion } from "flowbite-react";
import axios from 'axios';
import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import getTimeFromTimeStamp from './utils/getTimeFromTimeStamp.ts';
import createDatePickerOption from './utils/createDatePickerOption.ts';

type TextItem = {
  text: string;
  timestamp: string;
};

type FileItem = {
  url: string;
  timestamp: string;
};

function App() {
  const [items, setItems] = useState<any>(null);
  const [feedback, setFeedback] = useState<string>('');
  const [selectedDate, setSelectedDate] = useState(new Date());

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
      const requestBody = {
        user_id: user_id,
        year: year,
        month: month,
        day: day,
      };
      const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/diary/fetch_diary`, requestBody);
      setItems(response.data);
      setFeedback(response.data.feedback);
    } catch (err) {
      setItems([]);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const user_id = urlParams.get('user_id');
      const year = selectedDate.getFullYear();
      const month = selectedDate.getMonth() + 1;
      const day = selectedDate.getDate();
      if (user_id) {
        await post_fetch_diary(user_id, year, month, day);
      }
    }

    fetchData();
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
            この日の記録はまだありません
          </div>
        </div>
      )}
      <div className="fixed bottom-0 left-0 z-50 w-full h-16 bg-white border-t border-gray-200 dark:bg-gray-700 dark:border-gray-600">
        <div className="grid h-full max-w-lg grid-cols-3 mx-auto font-medium">
            <Link to={`https://line.me/R/ti/p/${import.meta.env.VITE_LINE_BOT_ID}`} type="button" className="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group">
              <svg className="w-5 h-5 mb-2 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="200" height="181.456" viewBox="0 0 200 181.456"><g transform="translate(-13.637 -264.2)"><path d="M113.639,264.2c-55.229,0-100,34.066-100,76.09.008,33.182,28.282,62.534,69.863,72.535l10.91,32.832,28.051-29.627c51.58-3.477,91.137-36.338,91.175-75.739,0-42.023-44.77-76.089-100-76.09ZM76.918,331.153c6.082,0,11.013,4.656,11.015,10.4S83,351.962,76.918,351.962,65.9,347.3,65.9,341.556s4.933-10.4,11.017-10.4Zm36.721,0c6.082,0,11.013,4.656,11.015,10.4s-4.93,10.407-11.015,10.408-11.022-4.661-11.019-10.409S107.555,331.152,113.639,331.153Zm36.721,0c6.082,0,11.013,4.656,11.015,10.4s-4.93,10.407-11.015,10.408-11.022-4.661-11.019-10.409S144.276,331.152,150.359,331.153Z" transform="translate(0)"/></g></svg>
              <span className="text-sm text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500">LINEに戻る</span>
            </Link>
            <Link
              to={diaryLink}
              className="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group"
            >
              <svg className="w-5 h-5 mb-2 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 17V2a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a2 2 0 0 0-2 2Zm0 0a2 2 0 0 0 2 2h12M5 15V1m8 18v-4"/>
              </svg>
              <span className="text-sm text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500">Diary</span>
            </Link>
            <Link to={profileLink} type="button" className="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group">
              <svg className="w-5 h-5 mb-2 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
              </svg>
              <span className="text-sm text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500">Profile</span>
            </Link>
        </div>
      </div>
    </div>
  )
}

export default App
