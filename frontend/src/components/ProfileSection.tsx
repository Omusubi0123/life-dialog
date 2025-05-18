import { ProfileData } from '../types/profile';

type Props = {
  profile: ProfileData;
};

export default function ProfileSection({ profile }: Props) {
  return (
    <div id="a" className="mt-10 mb-20 mx-10">
      <div className="flex items-center gap-4 mb-10">
        {profile.iconUrl && (
          <img className="w-20 h-20 rounded-full" src={profile.iconUrl} alt="" />
        )}
        <div className="font-semibold dark:text-white">
          <div className="text-lg text-gray-800 dark:text-white">{profile.name}</div>
          {profile.createdAt && profile.updatedAt && (
            <div className="text-sm text-gray-500 dark:text-gray-400">
              {profile.createdAt} to {profile.updatedAt}
            </div>
          )}
        </div>
      </div>
      <div className="mb-8">
        <div className="flex items-center mb-4">
          <h3 className="text-xl font-semibold text-gray-800 dark:text-white">あなたは...</h3>
        </div>
        <p className="text-gray-800">{profile.personality}</p>
      </div>
      <div className="mb-8">
        <div className="flex items-center mb-4">
          <svg
            className="w-6 h-6 text-green-500 mr-2"
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" strokeWidth="2" />
            <path
              d="M9 12l2 2 4-4"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <h3 className="text-xl font-semibold text-gray-600 dark:text-white">あなたの強み</h3>
        </div>
        <p className="text-gray-800">{profile.strength}</p>
      </div>
      <div className="mb-8">
        <div className="flex items-center mb-4">
          <svg
            className="w-6 h-6 text-yellow-500 mr-2"
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm0 14a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zm0-9c.69 0 1.25.56 1.25 1.25v5.5a1.25 1.25 0 1 1-2.5 0v-5.5C10.75 7.56 11.31 7 12 7z" />
          </svg>
          <h3 className="text-xl font-semibold text-gray-800 dark:text-white">あなたの弱み</h3>
        </div>
        <p className="text-gray-800">{profile.weakness}</p>
      </div>
    </div>
  );
}
