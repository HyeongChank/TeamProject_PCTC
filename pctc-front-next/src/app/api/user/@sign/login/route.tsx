import validUser from "@/app/components/server/validUser";
import { redirect } from "next/navigation";
import withSession from "next-auth";
import { NextResponse } from "next/server";
import { equal } from "assert";

type parameterType = {
  [key: string]: any
}

export async function GET(request: Request) {
  // console.log(request.body)
  return redirect('/');
}

export async function POST(request: Request) {
  const reader = request.body?.pipeThrough(new TextDecoderStream()).getReader();
  const inReader = await reader?.read();
  const { done, value } = inReader ?? { done: true, value: null };
  const parameters = JSON.parse(value ?? "{}");
  const user = await validUser(parameters?.userID);
  let user2 = {...user} ?? {};

  if (validLogin(parameters, user)) {
    // 로그인 성공
    return new NextResponse(JSON.stringify({
      "islogin": true,
      "user": user2
    }));
  } else {
    // 로그인 실패
    return new NextResponse(JSON.stringify({
      "islogin": false
    }));
  }
}

function validLogin(parameters: any, user: any) {
  if (parameters?.userID == user[0]?.id && parameters?.userPW == user[0]?.pw)
    return true;

  return false;
}

