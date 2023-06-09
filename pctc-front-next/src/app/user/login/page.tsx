"use client";
import { getCookie } from "@/function/cookie/GetCookie";
import { socialLogin } from "@/function/signin/SocialLogin";
import Image from "next/image";
import { useEffect, useRef, useState } from "react";

export default function Login() {
  // 로그인 이력(쿠키, 로컬스토리지)이 있는지 확인.
  // socialLogined();

  const [loginSession, setLoginSession] = useState({
    state: getCookie("islogin")?.toString(),
    name: decodeURIComponent(getCookie('username') as string),
  });

  

  const userID = useRef<HTMLInputElement>(null);
  const userPW = useRef<HTMLInputElement>(null);


  function submitKey(e: any) {
    if (e.keyCode === 13) {
      e.preventDefault();
      submit();
    }
  }

  async function submit() {
    // if (process.env.NODE_ENV === "development") {
      if (true) {
      const res = await fetch("http://10.125.121.222:8080/user/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: userID.current?.value,
          password: userPW.current?.value,
        }),
      });
      
      if (res.status === 200) {
        const resettingLoginStatus = await import('./resettingLoginStatus');
        const { token, username } = await res.json();

        resettingLoginStatus.resettingLoginStatus(username, token);
      }
    }
  }

  /**
   * 소셜로그인 사이트로 이동
   * @param provider 
   */
  const handleSocialLogin = (provider: string) => {
    socialLogin(provider);
  };

  useEffect(() => {}, [loginSession]);

  return (
    <>
      <div id="loginPage" className="flex flex-col items-center mt-4 p-4">
        <article>
          <h1>로그인</h1>
          <input
            type="text"
            name="user-id"
            ref={userID}
            placeholder="아이디를 입력하세요."
          />
          <input
            type="password"
            name="user-pw"
            onKeyDown={submitKey}
            ref={userPW}
            placeholder="비밀번호를 입력하세요."
          />
          <button
            type="button"
            id="loginbtn"
            onClick={submit}
            className="bg-gray-700 hover:bg-gray-900 text-white font-bold py-2 px-4 rounded"
          >
            로그인
          </button>

          <button
            onClick={() => {
              handleSocialLogin("kakao");
            }}
          >
            <Image
              src="/kakao_login_large_narrow.png"
              width={244}
              height={60}
              alt="kakao login"
            />
          </button>

          <button
            onClick={() => {
              handleSocialLogin("naver");
            }}
          >
            <Image
              src="/naver_login_large_narrow.png"
              width={244}
              height={60}
              alt="naver login"
            />
          </button>

          <button
            onClick={() => {
              handleSocialLogin("google");
            }}
          >
            <Image
              src="/google_login_large_narrow.png"
              width={244}
              height={60}
              alt="google login"
            />
          </button>
        </article>
      </div>
      <style jsx>{`
        div {
          display: flex;
          flex-direction: column;
          align-items: center;
          margin-top: 4rem;
          padding: 1rem;
        }
        article {
          width: 25rem;
          height: 40.45rem;
          display: flex;
          flex-direction: column;
          align-items: center;
          margin-top: 1rem;
          padding: 1rem;
          padding-top: 3rem;
          border: 2px solid #282828;
          border-radius: 0.5rem;
        }
        h1 {
          text-align: center;
          font-size: 2.5rem;
          font-weight: 700;
          margin-bottom: 4rem;
        }
        input[type="text"],
        input[type="password"] {
          width: 10rem;
          height: 1.5rem;
          border-bottom: 1px solid #282828;
          margin: 0.5rem;
        }
        button {
          margin-top: 1rem;
        }
        #loginbtn {
          margin-bottom: 2rem;
        }
      `}</style>
    </>
  );
}
