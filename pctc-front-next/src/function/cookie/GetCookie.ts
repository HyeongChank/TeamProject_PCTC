export function getCookie(name: string) {

  if (typeof window !== 'undefined') {
    var cookieString = document.cookie;
    var cookies = cookieString.split("; ");

    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i];
      var [cookieName, cookieValue] = cookie.split("=");

      if (cookieName === name) {
        return cookieValue;
      }
    }

    return null;
  }
  else
    console.log("클라이언트에서만 지원하는 함수입니다.");
}