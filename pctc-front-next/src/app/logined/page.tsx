"use client";

import { getURL } from "next/dist/shared/lib/utils";
import { useRouter } from "next/navigation";


export default function LoginedPage() {
  if (typeof window !== "undefined") {
    let search = window.location.search;
    let url = getURL();
    const token: string = url.split("?")[1];
    localStorage.setItem("ACCESS_TOKEN", token);
  }
  useRouter().push("/");
  return <></>;
}


/**
 * 이 페이지는 /user/login/page.js에 통합되어 삭제 예정
 */