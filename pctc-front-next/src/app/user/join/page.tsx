"use client";
import { getCookie } from "@/function/cookie/GetCookie";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { socialLogined } from "../login/socialLogined";

export default function Join() {
  const [loginSession, setLoginSession] = useState({
    state: getCookie("islogin")?.toString(),
    name: getCookie("name"),
  });

  const userID = useRef<HTMLInputElement>(null);
  const userPW = useRef<HTMLInputElement>(null);
  const userName = useRef<HTMLInputElement>(null);

  const router = useRouter();

  socialLogined();


  function submitKey(e: any) {
    if (e.keyCode === 13) {
      e.preventDefault();
      submit();
    }
  }

  async function submit() {
    if (process.env.NODE_ENV === "development") {
      const res = await fetch("http://10.125.121.222:8080/user/join", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: userID.current?.value,
          password: userPW.current?.value,
          nickname: userName.current?.value,
        }),
      });

      if(res.status === 200) {
        router.push("/user/login");
      }

      if(res.status === 409){
        alert("아이디 중복임 다시 적어");
      }
    }
  }

  useEffect(() => {}, [loginSession]);

  return (
    <>
      <div id="loginPage" className="flex flex-col items-center mt-4 p-4">
        <article>
          <h1>회원가입</h1>
          <input
            type="text"
            name="user-id"
            ref={userID}
            placeholder="아이디를 입력하세요."
          />
          <input
            type="password"
            name="user-pw"
            ref={userPW}
            placeholder="비밀번호를 입력하세요."
          />
          <input
            type="text"
            name="user-name"
            onKeyDown={submitKey}
            ref={userName}
            placeholder="이름을 입력하세요."
          />
          <button
            type="button"
            id="joinbtn"
            onClick={submit}
            className="bg-gray-700 hover:bg-gray-900 text-white font-bold py-2 px-4 rounded"
          >
            회원가입
          </button>

          <button>
            <Image
              src="/kakao_login_large_narrow.png"
              width={244}
              height={60}
              alt="Kakao login"
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
        #joinbtn {
          margin-bottom: 2rem;
        }
      `}</style>
    </>
  );
}
