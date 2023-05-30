import { makeTimeLabel, Time } from "@/function/util/makeTimeLabel";
import { cookies } from "next/dist/client/components/headers";
import Dashboard from "./Dashboard";

export default function Home() {
  let flag = true;
  // x축 5칸, interval 10분
  const timeLabel = makeTimeLabel(21, 10)?.map(
    (timeInstance: Time) => timeInstance.time
  );
  const dataLabel = [];

  if (timeLabel?.length) {
    for (let i = 0; i < timeLabel?.length; i++) {
      dataLabel.push(Math.random());
    }
  }

  if (cookies().get("isLogin")?.value === "true") {
    return (
      <main id="root-main">
        <Dashboard
          apiKey={process.env.KAKAO_MAP_API_KEY}
          dataLabel={dataLabel}
          timeLabel={timeLabel}
        />
      </main>
    );
  } else {
    return <main id="root-main"></main>;
  }
}
