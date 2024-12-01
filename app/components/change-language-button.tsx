"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { AlignJustifyIcon } from "lucide-react";
import { getCookie, setCookie } from "cookies-next";
// @components
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";

interface Props {
  select_language: {
    main: string;
    it: string;
    en: string;
  };
}

export function ChangeLanguageButton({ select_language }: Readonly<Props>) {
  const { refresh } = useRouter();

  useEffect(() => {
    if (!!getCookie("language") === false) {
      setCookie("language", "it");
    }
  }, []);

  const setItalianLanguage = () => {
    setCookie("language", "it");
    refresh();
  };

  const setEnglishLanguage = () => {
    setCookie("language", "en");
    refresh();
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="secondary" className="w-auto md:w-44 outline-none">
          <p className="hidden md:block">{select_language.main}</p>
          <AlignJustifyIcon
            className="block md:hidden"
            style={{ width: 20, height: 20 }}
          />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-auto md:w-44">
        <DropdownMenuItem
          className="cursor-pointer flex justify-between"
          onClick={setItalianLanguage}>
          {select_language.it}{" "}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/0/03/Flag_of_Italy.svg"
            className="w-6 h-6"
            alt="Italy"
          />
        </DropdownMenuItem>
        <DropdownMenuItem
          className="cursor-pointer flex justify-between"
          onClick={setEnglishLanguage}>
          {select_language.en}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Flag_of_the_United_Kingdom_%281-2%29.svg/1200px-Flag_of_the_United_Kingdom_%281-2%29.svg.png"
            className="w-6 h-6 object-cover"
            alt="United Kingdom"
          />
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
