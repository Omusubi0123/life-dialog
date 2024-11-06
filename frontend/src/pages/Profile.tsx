import '../index.css'
import { useEffect, useState } from 'react';
import {useLocation } from 'react-router-dom';
import axios from 'axios';
import parseDateString from '../utils/parseDateString.ts';
import Footer from '../components/Footer.tsx';

export default function Profile() {
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
      setUserName(response.data.name);
      setUserIconURL(response.data.icon_url);
      setUserPersonality(response.data.personality);
      setUserStrength(response.data.strength);
      setUserWeakness(response.data.weakness);
      setUserCreatedAt(parseDateString(response.data.created_at));
      setUserUpdatedAt(parseDateString(new Date().toISOString()));
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
      <Footer diaryLink={diaryLink} profileLink={profileLink} />
    </div>
  )
}
