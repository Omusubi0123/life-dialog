export default function parseDateString(dateString: string): string {
    const date = new Date(dateString);
    const year = date.getUTCFullYear();
    const month = String(date.getUTCMonth() + 1).padStart(2, '0'); // 月を2桁にする
    const day = String(date.getUTCDate()).padStart(2, '0'); // 日を2桁にする

    return `${year}-${month}-${day}`;
}