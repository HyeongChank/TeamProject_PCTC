export class Time {
  raw: number;
  year: number;
  month: number;
  days: number;
  hour: number;
  minute: number;
  second: number;
  time: string;
  constructor(point: Date) {
    this.raw = point.getTime();
    this.year = point.getFullYear();
    this.month = point.getMonth();
    this.days = point.getDate();
    this.hour = point.getHours();
    this.minute = point.getMinutes();
    this.second = point.getSeconds();
    this.time = point.toTimeString().split(' ')[0];
  }
}

/**
 * @param slice 차트의 시간축(x축)을 몇 등분 할 것인가? && 홀수만 입력 가능
 * @param interval 시간 축의 간격
 * @returns
 */
export function makeTimeLabel(slice: number, interval: number) : Time[] | undefined {
  if (slice < 1 || slice % 2 == 0) return;

  // 현재 시간 (중심축)
  const timeLine :Time[] = [];
  const center = Math.floor(slice / 2) + 1

  for(let i = 1; i <= slice; i++){
    timeLine.push(new Time(new Date(new Date().getTime() + (i - center) * interval * 60000)))
  }

  return timeLine;
}