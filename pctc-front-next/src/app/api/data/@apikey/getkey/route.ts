import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const reader = request.body?.pipeThrough(new TextDecoderStream()).getReader();
  const inReader = await reader?.read();
  const { done, value } = inReader ?? { done: true, value: null };

  const { token } = JSON.parse(value ?? "");

  if (token === "ABCDEFGH")
    return new NextResponse(process.env.KAKAO_MAP_API_KEY);
  else return new NextResponse("유효하지 않은 요청");
}
