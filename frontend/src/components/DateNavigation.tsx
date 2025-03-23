import { Datepicker } from 'flowbite-react';
import createDatePickerOption from '../utils/createDatePickerOption';

type Props = {
  selectedDate: Date;
  onPreviousDay: () => void;
  onNextDay: () => void;
  onDateChange: (date: Date | null) => void;
};

export default function DateNavigation({ selectedDate, onPreviousDay, onNextDay, onDateChange }: Props) {
  return (
    <div className="fixed top-0 left-0 z-50 w-full h-20 bg-white border-t border-gray-200 dark:bg-gray-700 dark:border-gray-600 flex items-center justify-center space-x-4">
      <button
        onClick={onPreviousDay}
        className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <div className="text-gray-500">
        <Datepicker
          theme={createDatePickerOption()}
          showClearButton={false}
          onChange={onDateChange}
          value={selectedDate}
        />
      </div>
      <button
        onClick={onNextDay}
        className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  );
}
