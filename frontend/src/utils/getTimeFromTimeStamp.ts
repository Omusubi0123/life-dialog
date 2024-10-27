export default function getTimeFromTimeStamp(timestamp: string): string {
    const date = new Date(timestamp);
    let hours: number = date.getUTCHours() + 9;
    if (hours >= 24) {
        hours -= 24;
    }
    const formattedHours: string = String(hours).padStart(2, '0');
    const minutes = String(date.getUTCMinutes()).padStart(2, '0');
    return `${formattedHours}:${minutes}`;
}