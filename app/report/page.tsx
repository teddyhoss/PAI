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

export default async function ReportPage({ searchParams }: Readonly<Props>) {
  const { id } = await searchParams;

  return (
    <div className="w-full h-full p-12">
      <Card className="w-full h-full p-8 space-y-4">
        <CardTitle className="flex flex-wrap gap-4 justify-evenly">
          <p>Numero ID: {id}</p>
          <p>Urgenza: Alta</p>
          <p>Categoria: Emergenza</p>
        </CardTitle>
        <hr />
        <CardContent>
          <div>
            <h2 className="text-2xl">Spiegazione:</h2>
            <p>
              Un'auto è in fiamme in via Roma, situazione che richiede un
              intervento immediato per evitare il rischio di esplosioni o danni
              ad altre proprietà.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
