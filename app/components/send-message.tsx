"use client";
import { z } from "zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Loader2Icon } from "lucide-react";
import { zodResolver } from "@hookform/resolvers/zod";
// @components
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
// @hooks
import { useToast } from "@/hooks/use-toast";

interface Props {
  _form: {
    placeholder_input_message: string;
    placeholder_input_cap: string;
    error_required_input: string;
    button_submit: string;
    error_required_cap: string;
  };
  thank_you_for_your_feedback: {
    thank_you: string;
    phrase: string;
    button_submit: string;
  };
}

export function SendMessage({
  _form,
  thank_you_for_your_feedback,
}: Readonly<Props>) {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isDone, setIsDone] = useState(false);

  const refresh = () => {
    window.location.href = "/";
  };

  const { toast } = useToast();

  const schema = z.object({
    message: z.string().min(1, {
      message: _form.error_required_input,
    }),
    cap: z
      .string()
      .min(5, {
        message: _form.error_required_cap,
      })
      .max(5, {
        message: _form.error_required_cap,
      }),
  });

  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: {
      message: "",
      cap: "",
    },
  });

  const onSubmit = form.handleSubmit(async (values: z.infer<typeof schema>) => {
    setLoading(true);

    try {
      if (isNaN(Number(form.getValues("cap"))) === true) {
        form.setError("cap", { message: _form.error_required_cap });
        return;
      }

      const response = await fetch("/api/classify/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: values.message, cap: values.cap }),
      });

      const data = await response.json();

      if (data.error) {
        toast({
          title: "Something went wrong",
          description: data.error,
          variant: "destructive",
        });

        return;
      }

      const main_container_home_page = document.getElementById(
        "main-container-home-page",
      );

      if (main_container_home_page) {
        main_container_home_page.style.display = "none";
      }

      setIsDone(true);
    } catch (error) {
      toast({
        title: "Fatal error",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  });

  return (
    <>
      {isDone ? (
        <div className="space-y-16 flex flex-col items-center justify-center mt-[-220px]">
          <div className="space-y-6 text-center">
            <h2 className="text-4xl md:text-6xl">
              {thank_you_for_your_feedback.thank_you}
            </h2>
            <p className="text-4xl">{thank_you_for_your_feedback.phrase}</p>
          </div>
          <Button
            variant="secondary"
            onClick={() => refresh()}
            className="w-80 mt-32 h-16 rounded-3xl bg-[#2d62c8] text-white hover:text-black text-xl">
            {thank_you_for_your_feedback.button_submit}
          </Button>
        </div>
      ) : (
        <Form {...form}>
          <form
            className="w-full lg:w-[50%] mt-16 space-y-4"
            onSubmit={onSubmit}>
            <FormField
              control={form.control}
              name="cap"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder={`${_form.placeholder_input_cap}`}
                      style={{ fontSize: "1.125rem" }}
                      className="w-full bg-white rounded-3xl text-black h-14 p-6 placeholder:text-lg"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="message"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder={`${_form.placeholder_input_message}`}
                      style={{ fontSize: "1.125rem" }}
                      className="w-full bg-white rounded-3xl text-black h-24 p-6 placeholder:text-lg"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="w-full flex items-center justify-center">
              <Button
                variant="secondary"
                className="w-64 h-16 rounded-3xl bg-[#2d62c8] text-white hover:text-black text-xl">
                {loading ? (
                  <Loader2Icon className="animate-spin h-8 w-8" />
                ) : (
                  <>{_form.button_submit}</>
                )}
              </Button>
            </div>
          </form>
        </Form>
      )}
    </>
  );
}
