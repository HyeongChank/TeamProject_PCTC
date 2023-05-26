/**
 * 구조 : "/Home/Dashboard"
 */
'use client';

import ChartComponent from "./components/client/serviceview/ChartComponent";
import CPVS from "./components/client/serviceview/CPVS";

export default function Dashboard ({apiKey, dataLabel, timeLabel} : any) {
  return (
    <>
      <CPVS apiKey={apiKey ?? ""} />
        <section id="root-main-section">
          <ChartComponent
            data={dataLabel}
            labels={timeLabel ?? []}
            width={38}
            height={40}
          />
          <ChartComponent
            data={dataLabel}
            labels={timeLabel ?? []}
            width={38}
            height={40}
          />
        </section>
    </>
  );
}