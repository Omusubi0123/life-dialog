/**
 * トークンベースでのアカウント紐付けページ
 */

import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import axios from 'axios';
import Cookies from 'js-cookie';

const TokenLink: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { isAuthenticated, isLoading, user } = useAuth();
  const [linkLoading, setLinkLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const token = searchParams.get('token');

  useEffect(() => {
    if (!token) {
      setError('無効なリンクです。トークンが見つかりません。');
      return;
    }

    // 認証されていない場合はGoogleログインに誘導
    if (!isLoading && !isAuthenticated) {
      // トークンをセッションストレージに保存してログイン後に使用
      sessionStorage.setItem('pending_link_token', token);
      navigate('/login?redirect=token-link');
      return;
    }

      // 認証済みの場合は自動的に紐付けを実行
  if (isAuthenticated && token && !success && !linkLoading) {
    handleTokenLink();
  }
  }, [isAuthenticated, isLoading, token, navigate, success]);

  const handleTokenLink = async () => {
    if (!token) return;

    setLinkLoading(true);
    setError(null);

    try {
      const authToken = Cookies.get('access_token');
      if (!authToken) {
        throw new Error('認証トークンが見つかりません');
      }

      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/auth/link-with-token`,
        { token },
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      if (response.data.success) {
        // 新しいアクセストークンを保存
        Cookies.set('access_token', response.data.access_token, {
          expires: 7,
          secure: import.meta.env.PROD,
          sameSite: 'strict',
        });

        setSuccess(true);
        
        // 3秒後にメインページにリダイレクト
        setTimeout(() => {
          navigate('/');
        }, 3000);
      }
    } catch (err) {
      console.error('アカウント紐付けに失敗:', err);
      if (axios.isAxiosError(err)) {
        console.error('Response status:', err.response?.status);
        console.error('Response data:', err.response?.data);
        console.error('Request config:', err.config);
        
        const message = err.response?.data?.detail || 'アカウントの紐付けに失敗しました';
        setError(`エラー詳細: ${message} (ステータス: ${err.response?.status || 'unknown'})`);
      } else {
        console.error('Unexpected error:', err);
        setError(`予期しないエラーが発生しました: ${err instanceof Error ? err.message : 'Unknown error'}`);
      }
    } finally {
      setLinkLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <div className="flex items-center justify-center w-12 h-12 mx-auto bg-blue-100 rounded-full mb-4">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            </div>
            <h3 className="text-lg font-medium text-gray-900 text-center mb-2">認証状態確認中</h3>
            <p className="text-sm text-gray-600 text-center">
              認証状態を確認しています。しばらくお待ちください...
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <div className="flex items-center justify-center w-12 h-12 mx-auto bg-green-100 rounded-full mb-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 text-center mb-2">紐付け完了</h3>
            <p className="text-sm text-gray-600 text-center mb-4">
              GoogleアカウントとLINEアカウントの紐付けが完了しました！
            </p>
            <p className="text-xs text-gray-500 text-center">
              3秒後に日記ページに移動します...
            </p>
          </div>
        </div>
      </div>
    );
  }

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
            <h3 className="text-lg font-medium text-gray-900 text-center mb-2">紐付け失敗</h3>
            <p className="text-sm text-gray-600 text-center mb-4">{error}</p>
            <div className="space-y-2">
              <button
                onClick={() => navigate('/login')}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                ログインページに戻る
              </button>
              {token && (
                <button
                  onClick={handleTokenLink}
                  disabled={linkLoading}
                  className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {linkLoading ? '処理中...' : '再試行'}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (linkLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <div className="flex items-center justify-center w-12 h-12 mx-auto bg-blue-100 rounded-full mb-4">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            </div>
            <h3 className="text-lg font-medium text-gray-900 text-center mb-2">アカウント紐付け中</h3>
            <p className="text-sm text-gray-600 text-center">
              GoogleアカウントとLINEアカウントを自動的に紐付けています...
            </p>
            {user && (
              <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                <p className="text-xs text-gray-600 text-center">
                  🔗 紐付け中: {user.name} ({user.email})
                </p>
                <p className="text-xs text-gray-500 text-center mt-1">
                  ↕️ LINE アカウント
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default TokenLink;
