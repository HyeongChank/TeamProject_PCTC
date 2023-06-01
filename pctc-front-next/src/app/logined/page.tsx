"use client";

import { createCookie } from "@/function/cookie/CreateCookie";
import { getURL } from "next/dist/shared/lib/utils";
import { useRouter } from "next/navigation";

export default function LoginedPage() {
  console.log("111");
  if (typeof window !== "undefined") {
    let url = getURL();
    const splitURL: string[] = url.split("?");
    console.log("222");

    if (typeof splitURL[1] !== "undefined") {
      console.log("333");
      const token: string = splitURL[1].slice(0, splitURL[1].length - 8);
      const username: string = splitURL[2];
      createCookie({
        isLogin: true,
        user: {
          username: username,
          token: token,
        },
      });
      console.log("444");
    }
  }
  // useRouter().push("/");
  return <></>;
}
