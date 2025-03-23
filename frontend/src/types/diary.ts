export type MessageItem = {
    media_type: 'text' | 'image' | 'video' | 'audio';
    content: string;
    time: string;
  };
  
  export type DiaryResponse = {
    items: MessageItem[];
    summary: string;
    feedback: string;
  };
