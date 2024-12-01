import { Circle } from "./circle";
import { useTranslations } from "next-intl";

interface Props {
  totalReports: number;
  highUrgency: number;
  mostReportedAreas: string;
  mostFrequencyCategory: string;
}

export function Dashboard({
  totalReports,
  highUrgency,
  mostReportedAreas,
  mostFrequencyCategory,
}: Readonly<Props>) {
  const t = useTranslations("dashboard");

  return (
    <div className="w-screen px-8 md:px-28 relative">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white shadow-md rounded-lg p-4">
          <h2 className="text-gray-600 font-semibold">{t("reports")}</h2>
          <p className="text-xl text-gray-800">{totalReports}</p>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4">
          <h2 className="text-gray-600 font-semibold">{t("urgency")}</h2>
          <p className="text-xl text-gray-800">{highUrgency}</p>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4">
          <h2 className="text-gray-600 font-semibold">{t("zone")}</h2>
          <p className="text-xl text-gray-800">{mostReportedAreas}</p>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4">
          <h2 className="text-gray-600 font-semibold">{t("category")}</h2>
          <p className="text-xl text-gray-800">{mostFrequencyCategory}</p>
        </div>
      </div>
      {/* <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white shadow-md rounded-lg p-4 h-auto">
          <h2 className="text-gray-600 font-semibold mb-4">
            {t("category_distribution")}
          </h2>
          <div className="w-full h-80 flex items-center justify-center">
            <CategoryDistribution />
          </div>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4 h-auto">
          <h2 className="text-gray-600 font-semibold mb-4">
            {t("area_distribution")}
          </h2>
          <div className="w-full h-80 flex items-center justify-center">
            <AreaDistribution />
          </div>
        </div>
      </div> */}
      {/* <div className="bg-white shadow-md rounded-lg p-4">
        <h2 className="text-gray-600 font-semibold mb-4">
          {t("latest_reports")}
        </h2>
        <div className="w-full">
          <DataTable
            placeholder_input={t("table.placeholder_input")}
            columns={columns}
            data={[
              {
                id: 31,
                text: "Un'auto ha preso fuoco in via Roma",
                cap: "00100",
                classification: {
                  category: "emergency",
                  urgency: "high",
                  explanation:
                    "Un'auto è in fiamme in via Roma, situazione che richiede un intervento immediato per evitare il rischio di esplosioni o danni ad altre proprietà.",
                },
                timestamp: "2024-12-01T03:15:47.102928Z",
              },
            ]}
          />
        </div>
      </div> */}
      <br />
      <Circle />
    </div>
  );
}
