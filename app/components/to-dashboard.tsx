"use client";
import { Button } from "@/components/ui/button";

export function ToDashboard() {
  const toDashboard = () => {
    window.location.href = "/dashboard";
  };

  return (
    <Button onClick={toDashboard} variant="link" className="text-white">
      Dashboard
    </Button>
  );
}
