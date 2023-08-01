export function getFirstThreeWordsWithEllipsis(spaceSeparatedString) {
    // Split the space-separated string into an array of words
    const wordsArray = spaceSeparatedString.split(' ');
  
    // Get the first three elements of the array
    const firstThreeWords = wordsArray.slice(0, 3);
  
    // Join the first three words back into a space-separated string
    let resultString = firstThreeWords.join(' ');
  
    // If there are more than three words, append "..." at the end
    if (wordsArray.length > 3) {
      resultString += '...';
    }
  
    return resultString;
  }
  