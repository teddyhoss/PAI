"use client";
import { z } from "zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
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
import { Loader2Icon } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Props {
  _form: {
    placeholder_input_message: string;
    placeholder_input_cap: string;
    error_required_input: string;
    button_submit: string;
  };
}

export function SendMessage({ _form }: Readonly<Props>) {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { toast } = useToast();

  const schema = z.object({
    message: z.string().min(1, {
      message: _form.error_required_input,
    }),
    cap: z.string().min(1, {
      message: _form.error_required_input,
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
    // Fare il fetch
  });

  return (
    <Form {...form}>
      <form className="w-full lg:w-[65%] mt-32 space-y-4" onSubmit={onSubmit}>
        <FormField
          control={form.control}
          name="message"
          render={({ field }) => (
            <FormItem>
              <FormControl>
                <Input
                  {...field}
                  placeholder={`${_form.placeholder_input_message}...`}
                  style={{ fontSize: "1.125rem" }}
                  className="w-full bg-white text-black h-18 p-6 placeholder:text-lg"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="cap"
          render={({ field }) => (
            <FormItem>
              <FormControl>
                <Input
                  {...field}
                  placeholder={`${_form.placeholder_input_cap}...`}
                  style={{ fontSize: "1.125rem" }}
                  className="w-full bg-white text-black h-18 p-6 placeholder:text-lg"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button variant="secondary">
          {loading ? (
            <Loader2Icon className="animate-spin h-8 w-8" />
          ) : (
            <>{_form.button_submit}</>
          )}
        </Button>
      </form>
    </Form>
  );
}
