export function socialLogin(provider: any) {
  if (typeof window !== "undefined") {
    let backendHost = null;

    const hostname = window && window.location && window.location.hostname;

    if (hostname === "localhost" || hostname === "10.125.121.207") {
      backendHost = "http://10.125.121.222:8080/";
    }

    const API_BASE_URL = backendHost;

    window.location.href = API_BASE_URL + "oauth2/authorization/" + provider;
  }
}
