"use client";

import { ArrowLeft } from "lucide-react";

export function ToDashboard() {
  const toDashboard = () => {
    window.location.href = "/dashboard";
  };

  return (
    <button onClick={toDashboard} className="top-0 left-0 cursor-pointer">
      <ArrowLeft />
    </button>
  );
}
