/**
 * Google認証コールバックページ
 */

import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const AuthCallback: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { handleAuthCallback, isLoading, error, requiresLineLink } = useAuth();

  useEffect(() => {
    const code = searchParams.get('code');
    const state = searchParams.get('state');
    const errorParam = searchParams.get('error');

    if (errorParam) {
      console.error('Google認証エラー:', errorParam);
      navigate('/login?error=auth_failed');
      return;
    }

    if (!code) {
      console.error('認証コードが見つかりません');
      navigate('/login?error=missing_code');
      return;
    }

    // コールバック処理を実行
    handleAuthCallback(code, state || undefined);
  }, [searchParams, handleAuthCallback, navigate]);

  // 認証処理後のリダイレクト
  useEffect(() => {
    if (!isLoading && !error) {
      if (requiresLineLink) {
        navigate('/link-line-user');
      } else {
        navigate('/');
      }
    }
  }, [isLoading, error, requiresLineLink, navigate]);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <div className="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
              <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 text-center mb-2">認証エラー</h3>
            <p className="text-sm text-gray-600 text-center mb-4">{error}</p>
            <button
              onClick={() => navigate('/login')}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              ログインページに戻る
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <div className="flex items-center justify-center w-12 h-12 mx-auto bg-blue-100 rounded-full mb-4">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          </div>
          <h3 className="text-lg font-medium text-gray-900 text-center mb-2">認証処理中</h3>
          <p className="text-sm text-gray-600 text-center">
            Google認証の処理を行っています。しばらくお待ちください...
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthCallback;
