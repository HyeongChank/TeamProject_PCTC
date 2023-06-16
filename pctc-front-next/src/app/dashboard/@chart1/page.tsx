'use client'

import ChartComponent from "@/app/components/client/serviceview/ChartComponent";
import { makeTimeLabel, Time } from "@/function/util/makeTimeLabel";

export default async function Chart1Page() {

  // x축 5칸, interval 10분
  const timeLabel = makeTimeLabel(21, 10)?.map(
    (timeInstance: Time) => timeInstance.time
  );

  const res = await fetch("http://10.125.121.222:8080/gettruck");
  const result = await res.json() as [string, number][];
  // console.log(result);

  return (
    <>
      <ChartComponent
          title="시간대별 야드 내 외부트럭 수"
          legend={["시간대", "야드 내 외부트럭 수(대)"]}
          data={result}
          labels={timeLabel ?? []}
          width={38}
          height={40}
        />
    </>
  );
}
