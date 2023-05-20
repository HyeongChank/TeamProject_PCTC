'use client';

import { Chart } from 'chart.js/auto'
import { useEffect, useRef } from 'react';


interface ChartComponentProps {
  data: number[];
  labels: string[];
  width?: number;
  height?: number;
}

export default function ChartComponent({ data, labels, width, height }: any) {
  const chartRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (chartRef.current) {
      const ctx = chartRef.current.getContext('2d');
      if (ctx) {
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [
              {
                label: 'Chart Example',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
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

  return <canvas ref={chartRef} width="400px" height={height} />;
};