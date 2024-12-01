import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { NextIntlClientProvider } from "next-intl";
import { getLocale, getMessages } from "next-intl/server";
// @components
import { Header } from "./components/header";
import { Toaster } from "@/components/ui/toaster";

const inter = Inter({ weight: ["500"], subsets: ["latin"] });

export const metadata: Metadata = {
  title: "TellNow",
};

interface Props {
  children: React.ReactNode;
}

export default async function RootLayout({ children }: Readonly<Props>) {
  const locale = await getLocale();

  const messages = await getMessages();

  return (
    <html lang={locale}>
      <body
        className={`w-screen h-screen bg-background ${inter.className} flex flex-col text-white`}>
        <Header />
        <NextIntlClientProvider messages={messages}>
          <main className="flex flex-col items-center justify-center flex-grow px-6">
            {children}
          </main>
        </NextIntlClientProvider>
        <Toaster />
      </body>
    </html>
  );
}
