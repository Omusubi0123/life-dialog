/**
 * 認証が必要なルートのプロテクションコンポーネント
 */

import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { isAuthenticated as checkToken } from '../utils/authApi';
import SkeletonLoader from './SkeletonLoader';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading, requiresLineLink } = useAuth();
  const [initialCheck, setInitialCheck] = useState(true);

  // 初期トークンチェック
  useEffect(() => {
    if (!checkToken()) {
      // トークンがない場合は即座にリダイレクト（ローディング表示なし）
      setInitialCheck(false);
    } else {
      // トークンがある場合は認証確認
      setInitialCheck(false);
    }
  }, []);

  // トークンがない場合は即座にログインページへ
  if (initialCheck && !checkToken()) {
    return <Navigate to="/login" replace />;
  }

  // ローディング中はスケルトンローディング表示
  if (isLoading && checkToken()) {
    return <SkeletonLoader />;
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
