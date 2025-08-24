/**
 * 認証関連の型定義
 */

export interface GoogleAuthLoginResponse {
  auth_url: string;
  code_verifier: string;
}

export interface GoogleAuthCallbackResponse {
  access_token: string;
  user_info: {
    id: string;
    email: string;
    name: string;
    picture?: string;
  };
  requires_link: boolean;
}

export interface LinkLineUserRequest {
  line_user_id: string;
}

export interface LinkLineUserResponse {
  success: boolean;
  access_token: string;
}

export interface UserInfoResponse {
  google_id: string;
  email: string;
  name: string;
  picture?: string;
  line_user_id?: string;
  has_line_link: boolean;
}

export interface AuthStatusResponse {
  is_authenticated: boolean;
  requires_line_link: boolean;
  user_info?: UserInfoResponse;
}

export interface AuthState {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: UserInfoResponse | null;
  requiresLineLink: boolean;
  error: string | null;
}
