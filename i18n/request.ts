import { cookies } from "next/headers";
import { getCookie } from "cookies-next/server";
import { getRequestConfig } from "next-intl/server";

export default getRequestConfig(async () => {
  const language = (await getCookie("language", { cookies })) ?? "it";

  const locale = ["it", "en"].some((x) => x === language) ? language : "it";

  return {
    locale,
    messages: (await import(`../messages/${locale}.json`)).default,
  };
});
