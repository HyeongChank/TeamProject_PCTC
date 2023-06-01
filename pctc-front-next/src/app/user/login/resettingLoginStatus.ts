import { createCookie } from "@/function/cookie/CreateCookie";
import { getCookie } from "@/function/cookie/GetCookie";
import { goto } from "@/function/goto/Goto";
import { Dispatch, SetStateAction } from "react";

/**
   * 일반 / 소셜 로그인 최종 로그인처리 함수. 로그인 쿠키 생성.
   * @param username 
   * @param token 
   */
export function resettingLoginStatus(username: string, token: string) {
  createCookie({
    isLogin: true,
    user: {
      username: username,
      token: token,
    }
  })
  goto("/");
}