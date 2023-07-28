function decodeJwtToken(token) {
    const tokenParts = token.split('.');
    const base64Payload = tokenParts[1];
    const decodedPayload = atob(base64Payload);
    return JSON.parse(decodedPayload);
  }
  
  export { decodeJwtToken };
  