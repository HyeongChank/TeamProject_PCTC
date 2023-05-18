import validJoin from "@/app/components/server/validJoin";
import validUser from "@/app/components/server/validUser";
import { NextResponse } from "next/server";
import { validLogin } from "../../ValidLogin";

type parameterType = {
  [key: string]: any
}

export async function POST(request: Request) {
  const reader = request.body?.pipeThrough(new TextDecoderStream()).getReader();
  const inReader = await reader?.read();
  const { done, value } = inReader ?? { done: true, value: null };

  const parameters = JSON.parse(value ?? "{}");

  const user = await validUser(parameters?.id);

  console.log("user12312 >> ", user);
  console.log("param1238123 >> ", parameters);

  let user2 = { ...user } ?? {};
  if (validLogin(parameters, user)) {
    // 아이디 중복 회원가입 실패
    return new NextResponse(JSON.stringify({
      "isLogin": false,
      "error": 409
    }));
  } else {
    if (await validJoin(parameters)) {
      // 회원가입 성공
      return new NextResponse(JSON.stringify({
        "isLogin": true,
        "user": parameters
      }));
    } else {
      // 회원가입 실패
      return new NextResponse(JSON.stringify({
        "isLogin": false,
        "error": 400
      }));
    }
  }

}