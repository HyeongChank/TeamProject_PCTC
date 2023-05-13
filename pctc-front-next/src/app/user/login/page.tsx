'use client'
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

export default function Login() {

  const [loginSession, setLoginSession] = useState({
    state: sessionStorage.getItem("PCTCLoginSuccess"),
    name: sessionStorage.getItem("PCTCName")
  });

  const userID = useRef<HTMLInputElement>(null);
  const userPW = useRef<HTMLInputElement>(null);

  const router = useRouter();

  function submit(e: any) {
    if (e.keyCode === 13) {
      e.preventDefault();
      fetch('/api/user/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          userID: userID.current?.value,
          userPW: userPW.current?.value
        })
      }).then(response => response.json())
        .then(result => {
          console.log(result);
          sessionStorage.setItem("PCTCLoginSuccess", result?.islogin);
          sessionStorage.setItem("PCTCID", result?.user[0].id);
          sessionStorage.setItem("PCTCPW", result?.user[0].pw);
          sessionStorage.setItem("PCTCName", result?.user[0].name);
          setLoginSession({
            state: sessionStorage.getItem("PCTCLoginSuccess"),
            name: sessionStorage.getItem("PCTCName")
          });
          router.push("/");
        });
    }
  }

  useEffect(() => {

  }, [loginSession])

  return (
    <>
      <div className="flex flex-col items-center mt-4 p-4">
        <div className="flex flex-col items-center mt-4 p-4 border-2 border-gray-800 rounded-md w-96">
          <h1 className="text-4xl font-bold text-gray-800">로그인</h1>
          <input type="text" className="border-b border-gray-800 m-1" name="user-id" ref={userID} placeholder="아이디를 입력하세요." />
          <input type="password" className="border-b border-gray-800 m-1" name="user-pw" onKeyDown={submit} ref={userPW} placeholder="비밀번호를 입력하세요." />
        </div>
      </div>
    </>
  );
}