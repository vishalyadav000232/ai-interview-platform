import { Eye, EyeOff, Loader2, Lock, Mail, User } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { registerSchema, type RegisterFormData } from "../schemas/register/shemas";


export const RegisterForm = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    console.log("Register Data:", data);
  };

  return (
    <div className="w-full">
      <div className="rounded-[28px] border border-white/10 bg-white/[0.03] p-8 shadow-[0_20px_80px_rgba(0,0,0,.45)] backdrop-blur-xl">
        <div>
          <h2 className="text-4xl font-bold">
            Create{" "}
            <span className="bg-gradient-to-r from-violet-500 to-fuchsia-500 bg-clip-text text-transparent">
              Account
            </span>
          </h2>

          <p className="mt-3 text-gray-400">
            Start your AI interview journey today.
          </p>
        </div>

        <form
          onSubmit={handleSubmit(onSubmit)}
          noValidate
          className="mt-3 space-y-5"
        >
          <div>
            <label className="mb-2 block text-[12px] text-gray-400 font-medium">First Name</label>

            <div className="group relative">
              <User className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-500 transition group-focus-within:text-violet-400" />

              <input
                type="text"
                placeholder="Jhon"
                autoComplete="name"
                {...register("first_name")}
                className="w-full rounded-xl border border-white/10 bg-white/[0.04] py-2 pl-12 pr-2 outline-none transition-all duration-300 placeholder:text-gray-500 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20"
              />
            </div>

            {errors.first_name && (
              <p className="mt-2 text-sm text-red-400">
                {errors.first_name.message}
              </p>
            )}
          </div>
          <div>
            <label className="mb-2 block text-[12px] text-gray-400 font-medium">Last Name</label>

            <div className="group relative">
              <User className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-500 transition group-focus-within:text-violet-400" />

              <input
                type="text"
                placeholder="deo"
                autoComplete="name"
                {...register("last_name")}
                className="w-full rounded-xl border border-white/10 bg-white/[0.04] py-2 pl-12 pr-2 outline-none transition-all duration-300 placeholder:text-gray-500 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20"
              />
            </div>

            {errors.last_name && (
              <p className="mt-2 text-sm text-red-400">
                {errors.last_name.message}
              </p>
            )}
          </div>

          <div>
            <label className="mb-2 block text-[12px] text-gray-400 font-medium">
              Email Address
            </label>

            <div className="group relative">
              <Mail className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-500 transition group-focus-within:text-violet-400" />

              <input
                type="email"
                placeholder="you@example.com"
                autoComplete="email"
                {...register("email")}
                className="w-full rounded-xl border border-white/10 bg-white/[0.04] py-2 pl-12 pr-2 outline-none transition-all duration-300 placeholder:text-gray-500 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20"
              />
            </div>

            {errors.email && (
              <p className="mt-2 text-sm text-red-400">
                {errors.email.message}
              </p>
            )}
          </div>

          <div>
            <label className="mb-2 block text-[12px] text-gray-400 font-medium">Password</label>

            <div className="group relative">
              <Lock className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-500 transition group-focus-within:text-violet-400" />

              <input
                type={showPassword ? "text" : "password"}
                placeholder="••••••••"
                autoComplete="new-password"
                {...register("password")}
                className="w-full rounded-xl border border-white/10 bg-white/[0.04] py-2 pl-12 pr-2 outline-none transition-all duration-300 placeholder:text-gray-500 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20"
              />

              <button
                type="button"
                onClick={() => setShowPassword((p) => !p)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 transition hover:text-violet-400"
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5" />
                ) : (
                  <Eye className="h-5 w-5" />
                )}
              </button>
            </div>

            {errors.password && (
              <p className="mt-2 text-sm text-red-400">
                {errors.password.message}
              </p>
            )}
          </div>

          <div>
            <label className="mb-2 block text-[12px] text-gray-400 font-medium">
              Confirm Password
            </label>

            <div className="group relative">
              <Lock className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-500 transition group-focus-within:text-violet-400" />

              <input
                type={showConfirmPassword ? "text" : "password"}
                placeholder="••••••••"
                autoComplete="new-password"
                {...register("confirmPassword")}
                className="w-full rounded-xl border border-white/10 bg-white/[0.04] py-2 pl-12 pr-2 outline-none transition-all duration-300 placeholder:text-gray-500 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20"
              />

              <button
                type="button"
                onClick={() => setShowConfirmPassword((p) => !p)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 transition hover:text-violet-400"
              >
                {showConfirmPassword ? (
                  <EyeOff className="h-5 w-5" />
                ) : (
                  <Eye className="h-5 w-5" />
                )}
              </button>
            </div>

            {errors.confirmPassword && (
              <p className="mt-2 text-sm text-red-400">
                {errors.confirmPassword.message}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-violet-600 to-fuchsia-600 py-4 font-semibold transition-all duration-300 hover:scale-[1.02] hover:shadow-lg hover:shadow-violet-500/30 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmitting && <Loader2 className="h-5 w-5 animate-spin" />}
            {isSubmitting ? "Creating account..." : "Create Account"}
          </button>

          <p className="text-center text-sm text-gray-400">
            Already have an account?{" "}
            <Link
              to="/login"
              className="font-medium text-violet-400 hover:text-violet-300"
            >
              Sign in
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
};
