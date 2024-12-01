import { useTranslations } from "next-intl";
// @components
import { SendMessage } from "./components/send-message";

export default function HomePage() {
  const t = useTranslations("home");

  return (
    <>
      <div
        className="text-center space-y-8 mt-[-60px]"
        id="main-container-home-page">
        <h2 className="text-6xl md:text-8xl">{t("welcome")}</h2>
        <p className="text-2xl md:text-3xl">
          {t("paragraphs.first.before_main_word")}{" "}
          <b>{t("paragraphs.first.main_word")}</b>{" "}
          {t("paragraphs.first.after_main_word")}
          <br />
          {t("paragraphs.second.before_main_word")}{" "}
          <b>{t("paragraphs.second.main_word")}</b>{" "}
          {t("paragraphs.second.after_main_word")}
          <br />
          {t("paragraphs.third.before_main_word")}{" "}
          <b>{t("paragraphs.third.main_word")}</b>.
        </p>
      </div>
      <SendMessage
        _form={{
          placeholder_input_message: t("form.placeholder_input_message"),
          placeholder_input_cap: t("form.placeholder_input_cap"),
          error_required_input: t("form.error_required_input"),
          button_submit: t("form.button_submit"),
          error_required_cap: t("form.error_required_cap"),
        }}
        thank_you_for_your_feedback={{
          thank_you: t("thank_you_for_your_feedback.thank_you"),
          phrase: t("thank_you_for_your_feedback.phrase"),
          button_submit: t("thank_you_for_your_feedback.button_submit"),
        }}
      />
    </>
  );
}
