export function calculateDuration(startTimeString, endTimeString) {
    const startTime = new Date(startTimeString);
    const endTime = new Date(endTimeString);

    const diffInMinutes = Math.abs(Math.round((endTime - startTime) / 60000)); // Convert milliseconds to minutes

    const hours = Math.floor(diffInMinutes / 60);
    const minutes = diffInMinutes % 60;

    if (hours === 0) {
        return `${minutes} Minutes`;
    } else if (minutes === 0) {
        return `${hours} Hours`;
    } else {
        return `${hours} Hours ${minutes} Minutes`;
    }
}
  