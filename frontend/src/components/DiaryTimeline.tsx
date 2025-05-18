import { MessageItem } from '../types/diary';

type Props = {
  items: MessageItem[];
};

export default function DiaryTimeline({ items }: Props) {
  return (
    <ol className="relative border-s border-gray-200 dark:border-gray-700">
      {items.map((item, index) => (
        <li key={index} className="mb-3 ms-4">
          <div className="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
          <time className="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">{item.time}</time>
          {item.media_type === 'text' && (
            <p className="mb-2 text-base font-normal text-gray-500 dark:text-gray-400">{item.content}</p>
          )}
          {item.media_type === 'image' && (
            <img className="h-auto w-2/3 max-w-full rounded-lg" src={item.content} alt="" />
          )}
          {item.media_type === 'video' && (
            <video className="h-auto w-2/3 max-w-full rounded-lg" controls>
              <source src={item.content} type="video/mp4" />
            </video>
          )}
          {item.media_type === 'audio' && (
            <audio className="w-2/3 max-w-full" controls>
              <source src={item.content} type="audio/mp3" />
            </audio>
          )}
        </li>
      ))}
    </ol>
  );
}
