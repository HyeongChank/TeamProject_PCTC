"use client";

import { getURL } from "next/dist/shared/lib/utils";
import { useRouter } from "next/router";


export default function LoginedPage() {
  if (typeof window !== "undefined") {
    let search = window.location.search;
    let url = getURL();
    let params = new URLSearchParams(search);
    const token: string = url.split("?")[1];
    localStorage.setItem("ACCESS_TOKEN", token);
  }
  useRouter().push("/");
  return <></>;
}
