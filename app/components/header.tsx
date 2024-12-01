import Link from "next/link";
import Image from "next/image";
import { useTranslations } from "next-intl";
// @components
import { ChangeLanguageButton } from "./change-language-button";

export function Header() {
  const t = useTranslations("navbar");

  return (
    <header className="w-full flex items-center justify-between px-6 md:px-24 py-4">
      <Link href="/">
        <div className="flex items-center ml-8">
          <Image priority src="/TalkNow.png" alt="" width={100} height={100} />
          <div className="text-left">
            <p className="text-2xl">
              <b>TellNow</b>
            </p>
            <p className="text-xl">
              <b>Voices Matter</b>
            </p>
          </div>
        </div>
      </Link>
      <div className="space-x-5">
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
