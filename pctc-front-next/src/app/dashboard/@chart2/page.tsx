'use client'

import ChartComponent from "@/app/components/client/serviceview/ChartComponent";
import { makeTimeLabel, Time } from "@/function/util/makeTimeLabel";

export default async function Chart1Page() {

  // x축 5칸, interval 10분
  const timeLabel = makeTimeLabel(21, 10)?.map(
    (timeInstance: Time) => timeInstance.time
  );

  const res = await fetch("http://10.125.121.222:8080/getpredict");
  const result = await res.json() as [string, number][];
  // console.log(result);

  return (
    <>
      <ChartComponent
          title="Turn around time"
          legend={["입차 시간대", "Turn around time(분)"]}
          data={result}
          labels={timeLabel ?? []}
          width={38}
          height={40}
        />
    </>
  );
}
