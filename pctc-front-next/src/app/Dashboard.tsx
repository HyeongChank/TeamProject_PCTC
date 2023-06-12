/**
 * 구조 : "/Home/Dashboard"
 */
"use client";

import { makeTimeLabel, Time } from "@/function/util/makeTimeLabel";
import ChartComponent from "./components/client/serviceview/ChartComponent";
import CPVS from "./components/client/serviceview/CPVS";

export default function Dashboard({ apiKey }: any) {

  // x축 5칸, interval 10분
  const timeLabel = makeTimeLabel(21, 10)?.map(
    (timeInstance: Time) => timeInstance.time
  );

  return (
    <>
      <CPVS apiKey={apiKey ?? ""} />
      <section id="root-main-section">
        <ChartComponent
          title="시간대별 야드 내 외부트럭 수"
          legend={["시간대", "야드 내 외부트럭 수(대)"]}
          labels={timeLabel ?? []}
          width={38}
          height={40}
        />
        <ChartComponent
          title="Turn around time"
          legend={["입차 시간대", "Turn around time"]}
          labels={timeLabel ?? []}
          width={38}
          height={40}
        />
      </section>
    </>
  );
}
