import './index.css'
import { Datepicker } from "flowbite-react";
import { Accordion } from "flowbite-react";
import axios from 'axios';
import { useEffect, useState } from 'react';


function App() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const requestBody = {
          "user_id": "Uefd3135357f2b4550eb07d5a903fb9bb",
          "year": 2024,
          "month": 10,
          "day": 26
        };
      
        console.log(`${import.meta.env.VITE_BACKEND_URL}/diary/fetch_diary`);
        const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/diary/fetch_diary`, requestBody);
        setData(response.data);
        console.log(data);
      } catch (err) {
        console.log(err);
      }
    };

    fetchData();
  }, []);



  return (
    <div className="bg-white">
      <div className="fixed top-0 left-0 z-50 w-full h-20 bg-white border-t border-gray-200 dark:bg-gray-700 dark:border-gray-600 space-x-4 flex items-center justify-center">
        <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
          <div className="">
            <Datepicker />
          </div>
      
        <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <div className="mt-24 mb-20 mx-10 bg-white">
        <div className="mt-20 mb-5 bg-white" id="accordion-open" data-accordion="open">
          <Accordion>
            <Accordion.Panel>
              <Accordion.Title>この日は何をした日？</Accordion.Title>
              <Accordion.Content>
                <p className="mb-2 text-gray-500 dark:text-gray-400">日々の生活が忙しくなると、どうしても小さな楽しみやリフレッシュする時間を忘れがち。でも、こうして少し時間を取るだけで心が穏やかになるのを実感した。今後は意識して自分のための時間も大切にしていきたい。</p>
              </Accordion.Content>
            </Accordion.Panel>
          </Accordion>
        </div>


        <ol className="relative border-s border-gray-200 dark:border-gray-700">                  
          <li className="mb-3 ms-4">
            <div className="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
            <time className="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">9:02</time><span className="p-2 text-gray-600"># ご飯</span>
            <p className="mb-2 text-base font-normal text-gray-500 dark:text-gray-400">うどんを食べた</p>
          </li>
          <li className="mb-3 ms-4">
            <div className="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
            <time className="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">9:05</time><span className="p-2 text-gray-600"># ご飯</span>
            <p className="mb-2 text-base font-normal text-gray-500 dark:text-gray-400">朝ごはん美味しかった</p>
            <p className="mb-2 text-base font-normal text-gray-500 dark:text-gray-400">朝ごはん食べると、結構仕事が捗る</p>
          </li>
          <li className="mb-3 ms-4">
            <div className="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
            <time className="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">9:05</time><span className="p-2 text-gray-600"># 学校</span>
            <p className="mb-2 text-base font-normal text-gray-500 dark:text-gray-400">電磁気学の授業を受けた。少し退屈。久しぶりにガウスの発散定理とかをちゃんと勉強した気がする</p>
          </li>
          <li className="mb-3 ms-4">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                  <img className="h-auto max-w-full rounded-lg" src="https://flowbite.s3.amazonaws.com/docs/gallery/square/image.jpg" alt=""></img>
              </div>
              <div>
                  <img className="h-auto max-w-full rounded-lg" src="https://flowbite.s3.amazonaws.com/docs/gallery/square/image-1.jpg" alt=""></img>
              </div>
              <div>
                  <img className="h-auto max-w-full rounded-lg" src="https://flowbite.s3.amazonaws.com/docs/gallery/square/image-2.jpg" alt=""></img>
              </div>
              <div>
                  <img className="h-auto max-w-full rounded-lg" src="https://flowbite.s3.amazonaws.com/docs/gallery/square/image-3.jpg" alt=""></img>
              </div>
              <div>
                <img className="h-auto max-w-full rounded-lg" src="https://flowbite.s3.amazonaws.com/docs/gallery/square/image-3.jpg" alt=""></img>
              </div>
            </div>
          </li>
          <li className="mb-3 ms-4">
            <div className="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
            <time className="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">12:15</time><span className="p-2 text-gray-600"># 友達</span><span className="p-2 text-gray-600"># 学校</span>
            <p className="mb-2 text-base font-normal text-gray-500 dark:text-gray-400">あんどぅーと昼ごはん食べに行った。学食500円以下でほっけ定食食べれた。久しぶりに魚食べたかも。美味かった</p>
          </li>
        </ol>
      </div>


      <div className="fixed bottom-0 left-0 z-50 w-full h-16 bg-white border-t border-gray-200 dark:bg-gray-700 dark:border-gray-600">
        <div className="grid h-full max-w-lg grid-cols-2 mx-auto font-medium">
            <a href="./index.html" type="button" className="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group">
                <svg className="w-5 h-5 mb-2 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 17V2a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a2 2 0 0 0-2 2Zm0 0a2 2 0 0 0 2 2h12M5 15V1m8 18v-4"/>
                </svg>
                <span className="text-sm text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500">Diary</span>
            </a>
            <a href="./profile.html" type="button" className="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group">
                <svg className="w-5 h-5 mb-2 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                </svg>
                <span className="text-sm text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500">Profile</span>
            </a>
        </div>
      </div>

    </div>
  )
}

export default App
