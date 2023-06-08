"use client";

import { Chart } from "chart.js/auto";
import { useEffect, useRef } from "react";
import { ChartComponentProps } from "./ChartComponent"

export default function ChartTotalEmptyContainer({
  title,
  legend,
  data,
  labels,
  width,
  height,
}: ChartComponentProps) {
  const chartRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (chartRef.current) {
      const ctx = chartRef.current.getContext("2d");
      if (ctx) {
        new Chart(ctx, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [
              {
                label: "선사별 공컨테이너",
                data: data,
                backgroundColor: "rgba(75, 192, 192, 0.6)",
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
          width: ${width}vw;
          height: ${height}vh;
        }
        canvas {
          width: ${width}vw;
          height: ${height}vh;
        }
      `}</style>
    </>
  );
}
