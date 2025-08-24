/**
 * 認証機能のカスタムフック
 */

import { useState, useEffect, useCallback } from 'react';
import { AuthState } from '../types/auth';
import {
  startGoogleAuth,
  handleGoogleCallback,
  linkLineUser,
  getAuthStatus,
  saveToken,
  removeToken,
  isAuthenticated as checkAuthenticated,
} from '../utils/authApi';

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    isLoading: true,
    user: null,
    requiresLineLink: false,
    error: null,
  });

  /**
   * 認証状態を初期化
   */
  const initializeAuth = useCallback(async () => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    if (!checkAuthenticated()) {
      setAuthState({
        isAuthenticated: false,
        isLoading: false,
        user: null,
        requiresLineLink: false,
        error: null,
      });
      return;
    }

    try {
      const status = await getAuthStatus();
      const user = status.user_info || null;

      setAuthState({
        isAuthenticated: status.is_authenticated,
        isLoading: false,
        user,
        requiresLineLink: status.requires_line_link,
        error: null,
      });
    } catch (error) {
      console.error('認証状態の取得に失敗:', error);
      setAuthState({
        isAuthenticated: false,
        isLoading: false,
        user: null,
        requiresLineLink: false,
        error: '認証状態の確認に失敗しました',
      });
    }
  }, []);

  /**
   * Google認証を開始
   */
  const loginWithGoogle = useCallback(async () => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }));
      
      const authData = await startGoogleAuth();
      
      // code_verifierをセッションストレージに保存
      sessionStorage.setItem('google_code_verifier', authData.code_verifier);
      
      // Googleの認証ページにリダイレクト
      window.location.href = authData.auth_url;
    } catch (error) {
      console.error('Google認証の開始に失敗:', error);
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: 'Google認証の開始に失敗しました',
      }));
    }
  }, []);

  /**
   * Google認証のコールバック処理
   */
  const handleAuthCallback = useCallback(async (code: string, state?: string) => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

      const savedCodeVerifier = sessionStorage.getItem('google_code_verifier');
      sessionStorage.removeItem('google_code_verifier');

      if (state && savedCodeVerifier && state !== savedCodeVerifier) {
        throw new Error('State parameter mismatch - possible CSRF attack');
      }

      const result = await handleGoogleCallback(code, state);
      
      // トークンを保存
      saveToken(result.access_token);

      if (result.requires_link) {
        setAuthState({
          isAuthenticated: true,
          isLoading: false,
          user: {
            google_id: result.user_info.id,
            email: result.user_info.email,
            name: result.user_info.name,
            picture: result.user_info.picture,
            has_line_link: false,
          },
          requiresLineLink: true,
          error: null,
        });
      } else {
        // 認証状態を再取得
        await initializeAuth();
      }
    } catch (error) {
      console.error('認証コールバックの処理に失敗:', error);
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: '認証処理に失敗しました',
      }));
    }
  }, [initializeAuth]);

  /**
   * LINE ユーザーIDとの紐付け
   */
  const linkToLineUser = useCallback(async (lineUserId: string) => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

      const result = await linkLineUser(lineUserId);
      
      if (result.success) {
        // 新しいトークンを保存
        saveToken(result.access_token);
        
        // 認証状態を再取得
        await initializeAuth();
      } else {
        throw new Error('LINE ユーザーの紐付けに失敗しました');
      }
    } catch (error) {
      console.error('LINE ユーザーの紐付けに失敗:', error);
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: 'LINE ユーザーの紐付けに失敗しました',
      }));
    }
  }, [initializeAuth]);

  /**
   * ログアウト
   */
  const logout = useCallback(() => {
    removeToken();
    setAuthState({
      isAuthenticated: false,
      isLoading: false,
      user: null,
      requiresLineLink: false,
      error: null,
    });
  }, []);

  /**
   * エラーをクリア
   */
  const clearError = useCallback(() => {
    setAuthState(prev => ({ ...prev, error: null }));
  }, []);

  // 初期化
  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  return {
    ...authState,
    loginWithGoogle,
    handleAuthCallback,
    linkToLineUser,
    logout,
    clearError,
    refresh: initializeAuth,
  };
};
