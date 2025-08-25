/**
 * 認証関連のAPIクライアント
 */

import axios from 'axios';
import Cookies from 'js-cookie';
import {
  GoogleAuthLoginResponse,
  GoogleAuthCallbackResponse,
  LinkLineUserResponse,
  UserInfoResponse,
  AuthStatusResponse,
} from '../types/auth';

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

// Axiosインスタンスを作成
const authApi = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// リクエストインターセプター：JWTトークンを自動的に追加
authApi.interceptors.request.use((config) => {
  const token = Cookies.get('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// レスポンスインターセプター：401エラー時にトークンを削除
authApi.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      Cookies.remove('access_token');
      // ログインページにリダイレクト
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Google OAuth認証開始
 */
export const startGoogleAuth = async (): Promise<GoogleAuthLoginResponse> => {
  const response = await authApi.get<GoogleAuthLoginResponse>('/auth/google/login');
  return response.data;
};

/**
 * Google OAuth コールバック処理
 */
export const handleGoogleCallback = async (
  code: string,
  state?: string
): Promise<GoogleAuthCallbackResponse> => {
  const response = await authApi.post<GoogleAuthCallbackResponse>('/auth/google/callback', {
    code,
    state,
  });
  return response.data;
};

/**
 * LINE ユーザーIDとの紐付け
 */
export const linkLineUser = async (lineUserId: string): Promise<LinkLineUserResponse> => {
  const response = await authApi.post<LinkLineUserResponse>('/auth/link-line-user', {
    line_user_id: lineUserId,
  });
  return response.data;
};

/**
 * 現在のユーザー情報を取得
 */
export const getCurrentUser = async (): Promise<UserInfoResponse> => {
  const response = await authApi.get<UserInfoResponse>('/auth/me');
  return response.data;
};

/**
 * 認証状態を取得
 */
export const getAuthStatus = async (): Promise<AuthStatusResponse> => {
  const response = await authApi.get<AuthStatusResponse>('/auth/status');
  return response.data;
};

/**
 * トークンを保存
 */
export const saveToken = (token: string): void => {
  Cookies.set('access_token', token, {
    expires: 7, // 7日間
    secure: import.meta.env.PROD,
    sameSite: 'strict',
  });
};

/**
 * トークンを取得
 */
export const getToken = (): string | undefined => {
  return Cookies.get('access_token');
};

/**
 * トークンを削除
 */
export const removeToken = (): void => {
  Cookies.remove('access_token');
};

/**
 * 認証済みかどうかを確認
 */
export const isAuthenticated = (): boolean => {
  return !!getToken();
};
