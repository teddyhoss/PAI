"use client";
import Link from "next/link";
import { EyeIcon } from "lucide-react";
import { getCookie } from "cookies-next";
import { ColumnDef } from "@tanstack/react-table";

const language = getCookie("language");

export type EmergencyReport = {
  id: number;
  text: string;
  cap: string;
  category: string;
  urgency: string;
  explanation: string;
  timestamp: string;
};

export const columns: ColumnDef<EmergencyReport>[] = [
  {
    accessorKey: "id",
    header: "ID",
  },
  {
    accessorKey: "cap",
    header: "Cap",
  },
  {
    accessorKey: "category",
    header: language === "it" ? "Categoria" : "Category",
  },
  {
    accessorKey: "urgency",
    header: language === "it" ? "Urgenza" : "Urgency",
  },
  {
    id: "action",
    cell: ({ row }) => {
      const id = row.original.id;

      return (
        <Link href={`/report?id=${id}`} replace>
          <EyeIcon className="w-6 h-6 cursor-pointer" />
        </Link>
      );
    },
  },
];
