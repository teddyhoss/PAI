import Link from "next/link";
// @components
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

export function Circle() {
  return (
    <div className="fixed bottom-10 right-10">
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger>
            <Link href="/chatbot" replace>
              <div className="w-20 h-20 rounded-full bg-black flex items-center justify-center">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src="https://developer-blogs.nvidia.com/wp-content/uploads/2024/08/llama-sunglasses-meadow.jpg"
                  alt="llama"
                  className="w-16 h-16 object-cover rounded-full"
                />
              </div>
            </Link>
          </TooltipTrigger>
          <TooltipContent>
            <div className="w-12 text-center">
              <p>Ciao, sono LLama IA e sto qui per aiutarti</p>
            </div>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </div>
  );
}
