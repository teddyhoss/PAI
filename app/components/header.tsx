import Link from "next/link";
import Image from "next/image";
import { useTranslations } from "next-intl";
// @components
import { ToDashboard } from "./to-dashboard";
import { ChangeLanguageButton } from "./change-language-button";

export function Header() {
  const t = useTranslations("navbar");

  return (
    <header className="w-full flex items-center justify-between px-12 py-4">
      <Link href="/">
        <div className="flex items-center">
          <Image priority src="/TalkNow.png" alt="" width={100} height={100} />
          <div className="text-left">
            <p className="text-2xl">TellNow</p>
            <p className="text-xl">Voices Matter</p>
          </div>
        </div>
      </Link>
      <div className="space-x-5">
        <ToDashboard />
        <ChangeLanguageButton
          select_language={{
            main: t("select-language.main"),
            it: t("select-language.it"),
            en: t("select-language.en"),
          }}
        />
      </div>
    </header>
  );
}
