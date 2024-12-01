// @components
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

export function Circle() {
  return (
    <div className="fixed bottom-10 right-10 z-[99999] flex flex-col items-center justify-center gap-2">
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger>
            <div className="w-20 h-20 rounded-full bg-[#2d62c8] flex items-center justify-center">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src="https://developer-blogs.nvidia.com/wp-content/uploads/2024/08/llama-sunglasses-meadow.jpg"
                alt="llama"
                className="w-16 h-16 object-cover rounded-full"
              />
            </div>
          </TooltipTrigger>
          <TooltipContent>
            <div className="w-24 text-center">
              <p>Ciao, sono LLama IA e sono qui per aiutarti</p>
            </div>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
      <div className="w-32 text-center bg-[#2d62c8] rounded-3xl text-white p-2">
        Llama chat
      </div>
    </div>
  );
}
