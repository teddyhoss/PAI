"use client";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";
import { Radar } from "react-chartjs-2";

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
);

export function CategoryDistribution() {
  const data = {
    labels: ["Fashion", "Cosmetics", "Watches", "Memes", "Technology"],
    datasets: [
      {
        label: "TikTok",
        data: [60, 40, 20, 70, 50],
        backgroundColor: "rgba(255, 205, 86, 0.2)",
        borderColor: "rgba(255, 205, 86, 1)",
        borderWidth: 2,
      },
      {
        label: "Twitter",
        data: [50, 45, 25, 55, 60],
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 2,
      },
      {
        label: "Facebook",
        data: [30, 35, 15, 65, 45],
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 2,
      },
    ],
  };

  return (
    <Radar
      data={data}
      options={{
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          tooltip: {
            enabled: true,
          },
        },
        scales: {
          r: {
            angleLines: {
              display: true,
            },
            suggestedMin: 0,
            suggestedMax: 100,
          },
        },
      }}
    />
  );
}
