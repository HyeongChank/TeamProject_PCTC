/**
 * 구조 : "/Home/Dashboard"
 */
"use client";

import ChartComponent from "./components/client/serviceview/ChartComponent";
import CPVS from "./components/client/serviceview/CPVS";

export default function Dashboard({ apiKey, dataLabel, timeLabel }: any) {
  return (
    <>
      <CPVS apiKey={apiKey ?? ""} />
      <section id="root-main-section">
        <ChartComponent
          title="시간대별 야드 내 외부트럭 수"
          legend={["시간대", "야드 내 외부트럭 수(대)"]}
          data={dataLabel}
          labels={timeLabel ?? []}
          width={38}
          height={40}
        />
        <ChartComponent
          title="Turn around time"
          legend={["입차 시간대", "Turn around time"]}
          data={dataLabel}
          labels={timeLabel ?? []}
          width={38}
          height={40}
        />
      </section>
    </>
  );
}
