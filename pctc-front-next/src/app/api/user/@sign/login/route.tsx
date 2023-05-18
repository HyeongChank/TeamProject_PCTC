import validUser from "@/app/components/server/validUser";
import { NextResponse } from "next/server";
import { validLogin } from "../../ValidLogin";

type parameterType = {
  [key: string]: any
}

type User = {
  id: string,
  pw: string,
  name: string;
}


export async function POST(request: Request) {
  const reader = request.body?.pipeThrough(new TextDecoderStream()).getReader();
  const inReader = await reader?.read();
  const { done, value } = inReader ?? { done: true, value: null };
  const parameters = JSON.parse(value ?? "{}");
  let user = await validUser(parameters?.id);
  user = JSON.stringify(user);
  console.log("user >> ", user);

  if (validLogin(parameters, user)) {
    // 로그인 성공
    return new NextResponse(JSON.stringify({
      "isLogin": true,
      "user": user,
    }));
  } else {
    // 로그인 실패
    return new NextResponse(JSON.stringify({
      "isLogin": false
    }));
  }
}