import { z } from "zod";

export const registerSchema = z.object({
  first_name: z
    .string()
    .trim()
    .min(1, "First name is required"),

  last_name: z
    .string()
    .trim()
    .min(1, "Last name is required"),

  email: z
    .string()
    .trim()
    .email("Please enter a valid email"),

  password: z
    .string()
    .min(1, "Enter the password")
    .min(8, "Password must be at least 8 characters long")
    .regex(/[A-Z]/, "Password must contain one uppercase letter")
    .regex(/[a-z]/, "Password must contain one lowercase letter")
    .regex(/[0-9]/, "Password must contain one number"),

    confirmPassword : z
    .string()
    .min(1, "Confirm password is required")
    .min(8, "Confirm password must be at least 8 characters long")
    .regex(/[A-Z]/, "Confirm password must contain one uppercase letter")
    .regex(/[a-z]/, "Confirm password must contain one lowercase letter")
    .regex(/[0-9]/, "Confirm password must contain one number"),
    
});


export type RegisterFormData = z.infer<typeof registerSchema>;