import YardStatus from "@/app/components/client/serviceview/YardStatus";
import { cookies } from "next/dist/client/components/headers";

export default async function BAS() {
  if (cookies().get("isLogin")?.value === "true") {
    return (
      <>
        <YardStatus apiKey={process.env.KAKAO_MAP_API_KEY} />
      </>
    );
  } else {
    return <></>;
  }
}
