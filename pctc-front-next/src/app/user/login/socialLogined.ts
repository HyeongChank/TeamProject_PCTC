import { getURL } from "next/dist/shared/lib/utils";


export function socialLogined(){
  if (typeof window !== "undefined") {
    let search = window.location.search;
    let url = getURL();
    const token: string = url.split("?")[1];
    localStorage.setItem("ACCESS_TOKEN", token);
  }
}

/**
 * http://localhost:3000/user/login
http://10.125.121.207:3000/user/login
http://10.125.121.222:8080/login/oauth2/code/kakao
	
http://localhost:8080/login/oauth2/code/kakao
 */