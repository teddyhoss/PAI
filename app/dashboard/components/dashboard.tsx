import { useTranslations } from "next-intl";
// @components
import { Circle } from "./circle";
import { DataTable } from "./data-table";
import { columns, EmergencyReport } from "./columns";
import { AreaDistribution } from "./area-distribution";
import { CategoryDistribution } from "./category-distribution";

interface Props {
  totalReports: number;
  highUrgency: number;
  mostReportedAreas: string;
  mostFrequencyCategory: string;
  data: Array<EmergencyReport>;
}

export function Dashboard({
  totalReports,
  highUrgency,
  mostReportedAreas,
  mostFrequencyCategory,
  data,
}: Readonly<Props>) {
  const t = useTranslations("dashboard");

  return (
    <div className="w-screen px-8 md:px-28 relative">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white shadow-md rounded-3xl p-4">
          <h2 className="font-semibold">{t("reports")}</h2>
          <p className="text-xl text-gray-800">{totalReports}</p>
        </div>
        <div className="bg-white shadow-md rounded-3xl p-4">
          <h2 className="font-semibold">{t("urgency")}</h2>
          <p className="text-xl text-gray-800">{highUrgency}</p>
        </div>
        <div className="bg-white shadow-md rounded-3xl p-4">
          <h2 className="font-semibold">{t("zone")}</h2>
          <p className="text-xl text-gray-800">{mostReportedAreas}</p>
        </div>
        <div className="bg-white shadow-md rounded-3xl p-4">
          <h2 className="font-semibold">{t("category")}</h2>
          <p className="text-xl text-gray-800">{mostFrequencyCategory}</p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white shadow-md rounded-3xl p-4 h-auto">
          <h2 className="font-semibold mb-4">{t("category_distribution")}</h2>
          <div className="w-full h-[32rem] flex items-center justify-center">
            <CategoryDistribution />
          </div>
        </div>
        <div className="bg-white shadow-md rounded-3xl p-4 h-auto">
          <h2 className="font-semibold mb-4">{t("area_distribution")}</h2>
          <div className="w-full h-[32rem] flex items-center justify-center">
            <AreaDistribution />
          </div>
        </div>
      </div>
      <div className="bg-white shadow-md rounded-3xl p-8 mb-12 flex flex-col items-center justify-center">
        <h2 className="font-semibold mb-4">{t("latest_reports")}</h2>
        <div className="w-[80%]">
          <DataTable
            placeholder_input={t("table.placeholder_input")}
            columns={columns}
            data={data}
          />
        </div>
      </div>
    </div>
  );
}
