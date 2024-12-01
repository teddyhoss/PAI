import { useTranslations } from "next-intl";
// @components
import { SendMessage } from "./components/send-message";

export default function HomePage() {
  const t = useTranslations("home");

  return (
    <>
      <div className="text-center space-y-8">
        <h2 className="text-6xl md:text-8xl">{t("welcome")}</h2>
        <p className="text-2xl md:text-3xl">
          {t("paragraphs.first.before_main_word")}{" "}
          <b>{t("paragraphs.first.main_word")}</b>
          {t("paragraphs.first.after_main_word")}
          <br />
          {t("paragraphs.second.before_main_word")}{" "}
          <b>{t("paragraphs.second.main_word")}</b>{" "}
          {t("paragraphs.second.after_main_word")}
          <br />
          {t("paragraphs.third.before_main_word")}{" "}
          <b>{t("paragraphs.third.main_word")}</b>
        </p>
      </div>
      <SendMessage
        _form={{
          placeholder_input_message: t("form.placeholder_input_message"),
          placeholder_input_cap: t("form.placeholder_input_cap"),
          error_required_input: t("form.error_required_input"),
          button_submit: t("form.button_submit"),
        }}
      />
    </>
  );
}
