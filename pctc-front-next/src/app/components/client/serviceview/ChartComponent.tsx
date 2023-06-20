"use client";

import { Chart } from "chart.js/auto";
import { useEffect, useRef } from "react";

export interface ChartComponentProps {
  title: string,
  legend: [string, string]
  data: [string, number][]
  labels: string[];
  width?: number;
  height?: number;
}

export default function ChartComponent({
  title,
  legend,
  data,
  labels,
  width,
  height,
}: ChartComponentProps) {
  const chartRef = useRef<HTMLCanvasElement>(null);

  const data1: any[] = []; // null 할당 해야하므로 number로 바꾸지 말것.
  const data2: any[] = [];

  for (let i = 1; i <= 21; i++) {
    if (i < 11) {
      data1.push(data?.[i-1]?.[1]);
      data2.push(null);
    } else if (i === 11) {
      data1.push(data?.[i-1]?.[1]);
      data2.push(data1[i-1]);
    } else {
      data1.push(null);
      data2.push(data?.[i-1]?.[1]);
    }
  }

  useEffect(() => {
    if (chartRef.current) {
      const ctx = chartRef.current.getContext("2d");
      if (ctx) {
        new Chart(ctx, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "실제 값",
                data: data1,
                backgroundColor: "rgba(75, 192, 192, 0.6)",
                fill: true,
              },
              {
                label: "예측 값",
                data: data2,
                backgroundColor: "rgba(255, 180, 150, 0.3)",
                fill: true,
                borderDash: [5, 5],
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              x: {
                beginAtZero: true,
                title: {
                  display: true,
                  align: 'end',
                  color: '#808080',
                  font: {
                    size: 12,
                  },
                  text: legend[0],
                }
                
              },
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  align: 'end',
                  color: '#808080',
                  font: {
                    size: 12,
                  },
                  text: legend[1],
                }
                
              },
            },
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: title,
                font: {
                  size: 30,
                  family: "'Gowun Dodum', 'Helvetica', 'Arial', sans-serif"
                }
              }
            },
          },
        });
      }
    }
  }, [labels]);

  return (
    <>
      <div>
        <canvas ref={chartRef} />
      </div>
      <style jsx>{`
        div {
          border: solid 1px #141414;
          border-radius: 7px;
          padding: 1rem;
          display: flex;
          justify-content: center;
        }
        canvas {
          width: ${width}vw;
          height: ${height}vh;
        }
      `}</style>
    </>
  );
}
