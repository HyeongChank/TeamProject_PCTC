import validJoin from "@/app/components/server/validJoin";
import validUser from "@/app/components/server/validUser";
import { NextResponse } from "next/server";

type parameterType = {
  [key: string]: any
}

export async function POST(request: Request) {
  const reader = request.body?.pipeThrough(new TextDecoderStream()).getReader();
  const inReader = await reader?.read();
  const { done, value } = inReader ?? { done: true, value: null };

  // console.log("회원가입 요청 정보 >> ", value);
  // 회원가입 요청 정보 >>  {"userID":"ghost","userPW":"1234","userName":"dbfud"}
  const parameters = JSON.parse(value ?? "{}");

  const user = await validUser(parameters?.userID);
  let user2 = {...user} ?? {};

  if (validLogin(parameters, user)) {
    // 아이디 중복 회원가입 실패
    return new NextResponse(JSON.stringify({
      "islogin": false,
      "error": 409
    }));
  } else {
    if (await validJoin(parameters)) {
      // 회원가입 성공
      return new NextResponse(JSON.stringify({
        "islogin": true,
        "user": parameters
      }));
    } else {
      // 회원가입 실패
      return new NextResponse(JSON.stringify({
        "islogin": false,
        "error": 400
      }));
    }
  }

}

function validLogin(parameters: any, user: any) {
  if (parameters?.userID == user[0]?.id && parameters?.userPW == user[0]?.pw)
    return true;

  return false;
}