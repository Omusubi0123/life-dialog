import './index.css'

function Profile() {
  return (
    <div className="bg-white">
        <div id="a" className="mt-10 mb-20 mx-10">
            <div className="flex items-center gap-4 mb-10">
                <img className="w-20 h-20 rounded-full" src="https://flowbite.s3.amazonaws.com/docs/gallery/square/image.jpg" alt=""></img>
                <div className="font-semibold dark:text-white">
                    <div className="text-lg text-gray-800 dark:text-white">山田吏月</div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">August 2023 to October 2024</div>
                </div>
            </div>

            <div className="mb-8">
            <div className="flex items-center mb-4">
                <h3 className="text-xl font-semibold text-gray-800 dark:text-white">あなたは...</h3>
            </div>
            <p className="text-gray-800">自立心が強いという特徴もあり、一人で何かをするのも気になりません。周りの人が自分に追いついてくるまで待つのを嫌うからかもしれません。何か決断をする際に他の人の意見などを聞くことも、通常、好みません。周りの人の考え・希望・計画を無視してしまうので、この“一匹狼”的な姿勢を無神経だと感じる人もいます。</p>
            </div>

            <div className="mb-8">
            <div className="flex items-center mb-4">
                <svg className="w-6 h-6 text-green-500 mr-2" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/>
                    <path d="M9 12l2 2 4-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <h3 className="text-xl font-semibold text-gray-600 dark:text-white">あなたの強み</h3>
            </div>
            <p className="text-gray-800">独立心と論理性を強く持ち、周囲に流されることなく、自分の道を突き進むタイプです。新しいアイデアや革新的なものを好み、既存の概念にとらわれない自由な発想を持っています</p>
            </div>

            <div className="mb-8">
            <div className="flex items-center mb-4">
                <svg className="w-6 h-6 text-yellow-500 mr-2" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm0 14a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zm0-9c.69 0 1.25.56 1.25 1.25v5.5a1.25 1.25 0 1 1-2.5 0v-5.5C10.75 7.56 11.31 7 12 7z"/>
                </svg>
                <h3 className="text-xl font-semibold text-gray-800 dark:text-white">あなたの弱み</h3>
            </div>
            <p className="text-gray-800">独立心と論理性を強く持ち、周囲に流されることなく、自分の道を突き進むタイプです。新しいアイデアや革新的なものを好み、既存の概念にとらわれない自由な発想を持っています</p>
            </div>

        </div>

        <div className="fixed bottom-0 left-0 z-50 w-full h-16 bg-white border-t border-gray-200 dark:bg-gray-700 dark:border-gray-600">
            <div className="grid h-full max-w-lg grid-cols-2 mx-auto font-medium">
                <a href="/" type="button" className="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group">
                    <svg className="w-5 h-5 mb-2 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 17V2a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a2 2 0 0 0-2 2Zm0 0a2 2 0 0 0 2 2h12M5 15V1m8 18v-4"/>
                    </svg>
                    <span className="text-sm text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500">Diary</span>
                </a>
                <a href="/profile" type="button" className="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group">
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

export default Profile
