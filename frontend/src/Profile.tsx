import './index.css'
import axios from 'axios';
import { useEffect, useState } from 'react';
import parseDateString from './utils/parseDateString.ts';
import { Link, useLocation } from 'react-router-dom';

function Profile() {
    const [userName, setUserName] = useState<any>(null);
    const [userIconURL, setUserIconURL] = useState<any>(null);
    const [userPersonality, setUserPersonality] = useState<any>(null);
    const [userStrength, setUserStrength] = useState<any>(null);
    const [userWeakness, setUserWeakness] = useState<any>(null);
    const [userCreatedAt, setUserCreatedAt] = useState<any>(null);
    const [userUpdatedAt, setUserUpdatedAt] = useState<any>(null);

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

    const get_fetch_profile = async (user_id: string) => {
        try {
            const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/user/fetch_profile`, {user_id: user_id});
            setUserName(response.data.user_name);
            setUserIconURL(response.data.icon_url);
            setUserPersonality(response.data.personality);
            setUserStrength(response.data.strength);
            setUserWeakness(response.data.weakness);
            setUserCreatedAt(parseDateString(response.data.created_at));
            setUserUpdatedAt(parseDateString(response.data.updated_at));
            console.log(parseDateString(response.data.created_at));
            console.log(parseDateString(response.data.updated_at));
            console.log()
        } catch (err) {
            console.log(err);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
          const urlParams = new URLSearchParams(window.location.search);
          const user_id = urlParams.get('user_id');
          if (user_id) {
            await get_fetch_profile(user_id);
          }
        }
    
        fetchData();
    }, []);


  return (
    <div className="bg-white">
        <div id="a" className="mt-10 mb-20 mx-10">
            <div className="flex items-center gap-4 mb-10">
                {userIconURL && (
                    <img className="w-20 h-20 rounded-full" src={userIconURL} alt=""></img>
                )}
                <div className="font-semibold dark:text-white">
                    <div className="text-lg text-gray-800 dark:text-white">{userName}</div>
                    {userCreatedAt && userUpdatedAt && (
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                            {userCreatedAt} to {userUpdatedAt}
                            </div>
                        )}
                    </div>
            </div>

            <div className="mb-8">
            <div className="flex items-center mb-4">
                <h3 className="text-xl font-semibold text-gray-800 dark:text-white">あなたは...</h3>
            </div>
            <p className="text-gray-800">{userPersonality}</p>
            </div>

            <div className="mb-8">
            <div className="flex items-center mb-4">
                <svg className="w-6 h-6 text-green-500 mr-2" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/>
                    <path d="M9 12l2 2 4-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <h3 className="text-xl font-semibold text-gray-600 dark:text-white">あなたの強み</h3>
            </div>
            <p className="text-gray-800">{userStrength}</p>
            </div>

            <div className="mb-8">
            <div className="flex items-center mb-4">
                <svg className="w-6 h-6 text-yellow-500 mr-2" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm0 14a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zm0-9c.69 0 1.25.56 1.25 1.25v5.5a1.25 1.25 0 1 1-2.5 0v-5.5C10.75 7.56 11.31 7 12 7z"/>
                </svg>
                <h3 className="text-xl font-semibold text-gray-800 dark:text-white">あなたの弱み</h3>
            </div>
            <p className="text-gray-800">{userWeakness}</p>
            </div>

        </div>
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

export default Profile
