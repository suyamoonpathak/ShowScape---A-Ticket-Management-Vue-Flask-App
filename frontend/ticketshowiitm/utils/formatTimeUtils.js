export function formatTime(datetimeString) {
    // Split the datetimeString by spaces
    if(datetimeString){
        const parts = datetimeString.split(' ');
    
        // Extract the time part from the parts array (last element without 'GMT')
        const timePart = parts[parts.length - 2];
    
        // Split the timePart by ':' to get hours and minutes
        const [hours, minutes] = timePart.split(':');
    
        // Format the time as needed (e.g., HH:mm format)
        const formattedTime = `${hours}:${minutes}`;
        console.log(formattedTime);
        return formattedTime;
    }
  }
  