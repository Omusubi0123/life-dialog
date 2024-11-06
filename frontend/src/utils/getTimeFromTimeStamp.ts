export function getTimeFromTimeStamp(timestamp: string): string {
    const date = new Date(timestamp);
    let hours: number = date.getUTCHours() + 9;
    if (hours >= 24) {
        hours -= 24;
    }
    const formattedHours: string = String(hours).padStart(2, '0');
    const minutes = String(date.getUTCMinutes()).padStart(2, '0');
    return `${formattedHours}:${minutes}`;
}

export default function getTimeFromDateString(dateString: string): string {
    const timePart = dateString.split(' ')[1];
    const [hours, minutes, seconts] = timePart.split(':');

    const formattedHours = hours.padStart(2, '0');
    const formatteeMinutes = minutes.padStart(2, '0');
    const formattedSeconds = seconts.padStart(2, '0');

    return `${formattedHours}:${formatteeMinutes}:${formattedSeconds}`;
}