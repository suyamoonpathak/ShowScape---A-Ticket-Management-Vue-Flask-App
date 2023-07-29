export function formatCSV(stringValue) {
    if (!stringValue || typeof stringValue !== 'string') {
      return '';
    }
  
    const stringList = stringValue.split(',').map(value => value.trim());
    return stringList.join(' | ');
  }