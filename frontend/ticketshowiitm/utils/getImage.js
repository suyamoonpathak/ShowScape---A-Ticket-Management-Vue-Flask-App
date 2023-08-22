function getImageUrl(filename) {
    return `${this.backendApiBaseUrl}/api/get_image/${filename}`;
  }
  export { getImageUrl };
  