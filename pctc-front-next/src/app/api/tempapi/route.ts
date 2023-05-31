import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const data = JSON.parse(`{"progress": "21", "order": "1", "name": "STAR RANGER(NSL)", "arrival": "2023/05/22 12:00", "departure": "2023/05/23 03:00", "unloading": "195/78/117", "loading": "169/0/169"}`);
  return NextResponse.json({data}, {status: 200})
}