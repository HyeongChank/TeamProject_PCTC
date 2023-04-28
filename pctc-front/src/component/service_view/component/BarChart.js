import React from "react";
import { Bar, Bubble } from 'react-chartjs-2'
import { Chart as ChartJS } from 'chart.js/auto'

const BarChart = ({chartData}) => {
  return <Bubble data={chartData} />;
}

export default BarChart;