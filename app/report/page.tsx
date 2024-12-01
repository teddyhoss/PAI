import {
  Card,
  CardContent,
  CardDescription,
  CardTitle,
} from "@/components/ui/card";
import { notFound } from "next/navigation";
import { ToDashboard } from "./components/to-dashboard";

import { getTranslations } from "next-intl/server";

interface Props {
  searchParams: Promise<{
    [key: string]: string | Array<string> | undefined;
  }>;
}

const getStats = async () => {
  const response = await fetch("http://localhost:8000/api/stats");

  const data = await response.json();

  if (data.error) {
    throw new data.error();
  }

  return data;
};

export default async function ReportPage({ searchParams }: Readonly<Props>) {
  const t = await getTranslations("report");

  try {
    const { id } = await searchParams;
    const stats = await getStats();

    const issue = stats.recent_issues.filter(
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (x: any) => x.id === Number(id),
    )[0];

    return (
      <div className="w-full md:w-[50%] h-full p-12">
        <Card className="w-full h-full p-8 space-y-4 rounded-3xl">
          <CardTitle className="flex flex-wrap gap-8">
            <div>
              <ToDashboard />
            </div>
            <div className="flex flex-grow gap-4 justify-evenly">
              <p>
                <span className="text-[#2d62c8]">{t("number")}:</span>{" "}
                {issue.id}
              </p>
              <p>
                <span className="text-[#2d62c8]">{t("urgency")}:</span>{" "}
                {issue.urgency}
              </p>
              <p>
                <span className="text-[#2d62c8]">{t("category")}:</span>{" "}
                {issue.category}
              </p>
            </div>
          </CardTitle>
          <br />
          <br />
          <br />
          <CardContent>
            <div>
              <h2 className="text-2xl text-[#2d62c8] font-bold">
                {t("summary")}:
              </h2>
              <p className="text-xl">{issue.explanation}</p>
              <br />
            </div>
            <hr />
            <br />
            <div>
              <h2 className="text-2xl text-[#2d62c8] font-bold">
                {t("issue")}:
              </h2>
              <p className="text-xl">{issue.text}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  } catch (error) {
    return notFound();
  }
}
