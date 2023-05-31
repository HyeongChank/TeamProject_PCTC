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
          title="시간대별 반출입 트럭 수"
          legend={["반출입 시간", "반출입 트럭 수"]}
          data={dataLabel}
          labels={timeLabel ?? []}
          width={38}
          height={40}
        />
        <ChartComponent
          title="반출입 시간대에 따른 대기시간"
          legend={["반출입 예측 시간", "대기 시간"]}
          data={dataLabel}
          labels={timeLabel ?? []}
          width={38}
          height={40}
        />
      </section>
    </>
  );
}
