"use client";
import { useState, useEffect } from "react";

interface Props {
  children: React.ReactNode;
  mountAfterMs?: number;
}

export function ClientOnly({ children, mountAfterMs }: Props) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (mountAfterMs !== undefined) {
      setTimeout(() => {
        setMounted(true);
      }, mountAfterMs);

      return;
    }

    setMounted(true);
  }, [mountAfterMs]);

  return mounted ? <>{children}</> : null;
}
