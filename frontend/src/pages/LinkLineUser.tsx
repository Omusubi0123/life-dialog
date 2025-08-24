/**
 * LINE ユーザーID紐付けページ
 */

import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

const LinkLineUser: React.FC = () => {
  const { user, linkToLineUser, isLoading, error, logout } = useAuth();
  const [lineUserId, setLineUserId] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!lineUserId.trim()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await linkToLineUser(lineUserId.trim());
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center">
            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
          LINE アカウントの紐付け
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          日記を閲覧するためにLINE ユーザーIDを紐付けてください
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {/* ユーザー情報表示 */}
          {user && (
            <div className="mb-6 p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center">
                {user.picture && (
                  <img
                    src={user.picture}
                    alt={user.name}
                    className="w-10 h-10 rounded-full mr-3"
                  />
                )}
                <div>
                  <p className="text-sm font-medium text-gray-900">{user.name}</p>
                  <p className="text-xs text-gray-600">{user.email}</p>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
              <span className="block sm:inline">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="lineUserId" className="block text-sm font-medium text-gray-700">
                LINE ユーザーID
              </label>
              <div className="mt-1">
                <input
                  id="lineUserId"
                  name="lineUserId"
                  type="text"
                  required
                  value={lineUserId}
                  onChange={(e) => setLineUserId(e.target.value)}
                  placeholder="例: U1234567890abcdef1234567890abcdef"
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  disabled={isLoading || isSubmitting}
                />
              </div>
              <p className="mt-2 text-xs text-gray-500">
                LINE Botでメッセージを送信した際のユーザーIDです。
                通常は「U」から始まる33文字の文字列です。
              </p>
            </div>

            <div>
              <button
                type="submit"
                disabled={isLoading || isSubmitting || !lineUserId.trim()}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isSubmitting ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    紐付け中...
                  </div>
                ) : (
                  'LINE ユーザーIDを紐付け'
                )}
              </button>
            </div>
          </form>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">または</span>
              </div>
            </div>

            <div className="mt-6">
              <button
                onClick={handleLogout}
                className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
              >
                別のGoogleアカウントでログイン
              </button>
            </div>
          </div>

          <div className="mt-6 text-xs text-gray-500 space-y-2">
            <p><strong>📱 LINE ユーザーIDの確認方法:</strong></p>
            <ol className="list-decimal list-inside space-y-1 ml-2">
              <li>LINE Botに何かメッセージを送信</li>
              <li>開発者にユーザーIDの確認を依頼</li>
              <li>上記のフォームに入力して紐付け</li>
            </ol>
            <p>
              ユーザーIDの確認が困難な場合は、管理者にお問い合わせください。
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LinkLineUser;
