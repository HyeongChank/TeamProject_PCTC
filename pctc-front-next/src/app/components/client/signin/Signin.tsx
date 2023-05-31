'use client'

import { deleteCookie } from '@/function/cookie/DeleteCookie';
import { getCookie } from '@/function/cookie/GetCookie';
import { goto } from '@/function/goto/Goto';
import Link from 'next/link';
import { useState, useEffect } from 'react'


export default function Signin() {
  // isLogin : 로그인 여부
  // setIsLogin : 로그인/로그아웃
  
  const [loginSession, setLoginSession] = useState({
    state: getCookie('isLogin')?.toString(),
    name: getCookie('username')
  });


  const [signinView, setSigninView] = useState(<>Log in</>); // 실제 Signin 컴포넌트 렌더링할 내용

  const translater = { // 번역기
    "kakao": "카카오",
    "naver": "네이버",
    "google": "구글",
    "카카오": "kakao",
    "네이버": "naver",
    "구글": "google",
    "로그인": "login",
    "login": "로그인",
    "회원가입": "join",
    "join": "회원가입",
  };

  function signout() {
    deleteCookie('isLogin')
    deleteCookie('name')
    deleteCookie('id')
    deleteCookie('pw')
    setLoginSession({
      state: "false",
      name: ""
    });
    goto('/')
  }
  
  useEffect(() => {
    if (loginSession.state === "true") {
      setSigninView(
        <div className='w-full h-full flex flex-col justify-center items-center'>
          <div className='w-32 text-base font-bold text-center'>
            <button>{loginSession.name} 님</button>
          </div>
          <div className='w-32 text-center'>
            <button onClick={signout}>Sign out</button>
          </div>
        </div>
      );
    } else {
      setSigninView(
        <div className='w-full h-full flex justify-center items-center'>
          <Link href='/user/login' style={{margin: "0.5rem"}}><button>Sign in</button></Link>
          <Link href='/user/join' style={{margin: "0.5rem"}}><button>Join</button></Link>
        </div>
      );
    }
  }, [loginSession]);

  return (
    <>
      {signinView}
    </>
  )
}