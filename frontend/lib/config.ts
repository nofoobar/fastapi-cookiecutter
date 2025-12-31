import { z } from "zod";

const envSchema = z.object({
  NEXT_PUBLIC_POSTHOG_ENABLED: z.enum(['true', 'false']).default('false'),
  NEXT_PUBLIC_POSTHOG_KEY: z.string().optional(),
  NEXT_PUBLIC_POSTHOG_HOST: z.string().optional(),
});

export const env = envSchema.parse(process.env);