/**
 * 認証が必要なルートのプロテクションコンポーネント
 */

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading, requiresLineLink } = useAuth();

  // ローディング中は読み込み画面を表示
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <div className="flex items-center justify-center w-12 h-12 mx-auto bg-blue-100 rounded-full mb-4">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            </div>
            <h3 className="text-lg font-medium text-gray-900 text-center mb-2">認証確認中</h3>
            <p className="text-sm text-gray-600 text-center">
              認証状態を確認しています。しばらくお待ちください...
            </p>
          </div>
        </div>
      </div>
    );
  }

  // 認証されていない場合はログインページにリダイレクト
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // LINE IDの紐付けが必要な場合は紐付けページにリダイレクト
  if (requiresLineLink) {
    return <Navigate to="/link-line-user" replace />;
  }

  // 認証済みの場合は子コンポーネントを表示
  return <>{children}</>;
};

export default ProtectedRoute;
