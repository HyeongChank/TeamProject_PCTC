export function socialLogin(provider: any){
  let backendHost = null;
  
  const hostname = window && window.location && window.location.hostname;
  
  if (hostname === "localhost") {
      backendHost = "http://localhost:8080/";
  }
  
  const API_BASE_URL = backendHost;
  
  window.location.href = API_BASE_URL + "oauth2/authorization/"+ provider;
}
