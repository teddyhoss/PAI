import {
  Card,
  CardContent,
  CardDescription,
  CardTitle,
} from "@/components/ui/card";

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
  const { id } = await searchParams;
  const stats = await getStats();

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const issue = stats.recent_issues.filter((x: any) => x.id === Number(id))[0];

  return (
    <div className="w-full h-full p-12">
      <Card className="w-full h-full p-8 space-y-4">
        <CardTitle className="flex flex-wrap gap-4 justify-evenly">
          <p>Numero ID: {issue.id}</p>
          <p>Urgenza: {issue.urgency}</p>
          <p>Categoria: {issue.category}</p>
        </CardTitle>
        <CardContent>
          <div>
            <h2 className="text-2xl">Problema:</h2>
            <p>{issue.explanation}</p>
            <br />
          </div>
          <hr />
          <br />
          <div>
            <h2 className="text-2xl">Segnalazione:</h2>
            <p>{issue.text}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
