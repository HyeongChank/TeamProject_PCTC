export function deleteCookie(name: string){
  if(window !== undefined)
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  else
    console.log("클라이언트에서만 지원하는 함수입니다.")
}