export function getFirstThreeTags(tagsString) {
    // Split the comma-separated tags string into an array
    const tagsArray = tagsString.split(',');
  
    // Get the first three elements of the array
    const firstThreeTags = tagsArray.slice(0, 3);
  
    // Join the first three tags back into a comma-separated string
    return firstThreeTags.join(',');
  }
  