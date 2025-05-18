import { useState } from 'react';

export const useDateControl = (initialDate: Date = new Date()) => {
  const [selectedDate, setSelectedDate] = useState<Date>(initialDate);

  const handlePreviousDay = () => {
    setSelectedDate((prev) => {
      const newDate = new Date(prev);
      newDate.setDate(prev.getDate() - 1);
      return newDate;
    });
  };

  const handleNextDay = () => {
    setSelectedDate((prev) => {
      const newDate = new Date(prev);
      newDate.setDate(prev.getDate() + 1);
      return newDate;
    });
  };

  const handleDateChange = (newDate: Date | null) => {
    if (newDate) setSelectedDate(newDate);
  };

  return {
    selectedDate,
    handlePreviousDay,
    handleNextDay,
    handleDateChange,
  };
};
