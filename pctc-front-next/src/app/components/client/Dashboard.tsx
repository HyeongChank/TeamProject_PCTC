'use client';

import ChartComponent from "./serviceview/ChartComponent";
import CPVS from "./serviceview/CPVS";

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