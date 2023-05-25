"use client";

import { Chart } from "chart.js/auto";
import { useEffect, useRef } from "react";

interface ChartComponentProps {
  data: number[];
  labels: string[];
  width?: number;
  height?: number;
}

export default function ChartComponent({
  data,
  labels,
  width,
  height,
}: ChartComponentProps) {
  const chartRef = useRef<HTMLCanvasElement>(null);

  const data1: any[] = [];
  const data2: any[] = [];

  for (let i = 1; i <= 21; i++) {
    if (i < 11) {
      data1.push(Math.random());
      data2.push(null);
    } else if (i === 11) {
      data1.push(Math.random());
      data2.push(data1[i-1]);
    } else {
      data1.push(null);
      data2.push(Math.random());
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
              },
              {
                label: "예측 값",
                data: data2,
                backgroundColor: "rgba(255, 180, 150, 0.6)",
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
              },
            },
          },
        });
      }
    }
  }, [data, labels]);

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
