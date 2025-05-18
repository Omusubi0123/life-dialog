import '../index.css';
import Footer from '../components/Footer';
import DateNavigation from '../components/DateNavigation';
import DiaryAccordion from '../components/DiaryAccordion';
import DiaryTimeline from '../components/DiaryTimeline';
import { useDiary } from '../hooks/useDiary';

export default function App() {
  const {
    items,
    summary,
    feedback,
    selectedDate,
    loading,
    handlePreviousDay,
    handleNextDay,
    handleDateChange,
    diaryLink,
    profileLink,
  } = useDiary();

  return (
    <div className="bg-white">
      <DateNavigation
        selectedDate={selectedDate}
        onPreviousDay={handlePreviousDay}
        onNextDay={handleNextDay}
        onDateChange={handleDateChange}
      />
      {items && items.items.length > 0 ? (
        <div className="mt-24 mb-20 mx-10 bg-white">
          <DiaryAccordion summary={summary} feedback={feedback} />
          <DiaryTimeline items={items.items} />
        </div>
      ) : (
        <div className="w-screen">
          <div className="flex items-center justify-center min-h-screen mb-2 text-base font-normal text-gray-500 dark:text-gray-400">
            {loading ? '読み込み中です...' : 'この日の記録はまだありません'}
          </div>
        </div>
      )}
      <Footer diaryLink={diaryLink} profileLink={profileLink} />
    </div>
  );
}