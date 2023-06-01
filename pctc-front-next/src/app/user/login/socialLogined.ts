import { createCookie } from "@/function/cookie/CreateCookie";
import { getURL } from "next/dist/shared/lib/utils";

export function socialLogined() {
  if (typeof window !== "undefined") {
    let search = window.location.search;
    let url = getURL();
    const splitURL: string[] = url.split("?");

    if (typeof splitURL[1] !== "undefined") {
      const token: string = splitURL[1].slice(0, splitURL[1].length - 8);
      const username: string = splitURL[2];
      localStorage.setItem("username", username);
      localStorage.setItem("token", token);
      localStorage.setItem("isLogin", "true");
      // createCookie({
      //   isLogin: true,
      //   user: {
      //     username: username,
      //     token: token,
      //   },
      // });

      // window.location.href = url;
    }
  }
}

/**
 * http://localhost:3000/user/login
http://10.125.121.207:3000/user/login
http://10.125.121.222:8080/login/oauth2/code/kakao
	
http://localhost:8080/login/oauth2/code/kakao
 */
