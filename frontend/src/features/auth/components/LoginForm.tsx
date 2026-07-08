import { Eye, EyeOff, Loader2, Lock, Mail } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, type LoginFormData } from "../schemas/login/schemas";


export const LoginForm = () => {
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    console.log(data);
  };

  return (
    <div className="w-full">
      <div className="rounded-[28px] border border-white/10 bg-white/[0.03] p-8 shadow-[0_20px_80px_rgba(0,0,0,.45)] backdrop-blur-xl">
        <div>
          <h2 className="text-4xl font-bold">
            Welcome{" "}
            <span className="bg-gradient-to-r from-violet-500 to-fuchsia-500 bg-clip-text text-transparent">
              Back!
            </span>
          </h2>

          <p className="mt-3 text-gray-400">
            Login to continue your interview journey.
          </p>
        </div>

        <form
          onSubmit={handleSubmit(onSubmit)}
          noValidate
          className="mt-8 space-y-6"
        >
          {/* Email */}

          <div>
            <label className="mb-2 block text-sm font-medium">
              Email Address
            </label>

            <div className="group relative">
              <Mail className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-500 transition group-focus-within:text-violet-400" />

              <input
                type="email"
                autoComplete="email"
                placeholder="you@example.com"
                {...register("email")}
                className="w-full rounded-xl border border-white/10 bg-white/[0.04] py-4 pl-12 pr-4 outline-none transition-all duration-300 placeholder:text-gray-500 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20"
              />
            </div>

            {errors.email && (
              <p className="mt-2 text-sm text-red-400">
                {errors.email.message}
              </p>
            )}
          </div>

          {/* Password */}

          <div>
            <label className="mb-2 block text-sm font-medium">
              Password
            </label>

            <div className="group relative">
              <Lock className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-500 transition group-focus-within:text-violet-400" />

              <input
                type={showPassword ? "text" : "password"}
                autoComplete="current-password"
                placeholder="••••••••"
                {...register("password")}
                className="w-full rounded-xl border border-white/10 bg-white/[0.04] py-4 pl-12 pr-12 outline-none transition-all duration-300 placeholder:text-gray-500 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20"
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

          <div className="flex justify-end">
            <Link
              to="/forgot-password"
              className="text-sm font-medium text-violet-400 hover:text-violet-300"
            >
              Forgot Password?
            </Link>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-violet-600 to-fuchsia-600 py-4 font-semibold transition-all duration-300 hover:scale-[1.02] hover:shadow-lg hover:shadow-violet-500/30 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmitting && (
              <Loader2 className="h-5 w-5 animate-spin" />
            )}

            {isSubmitting ? "Logging in..." : "Login"}
          </button>

          <div className="flex items-center gap-4">
            <div className="h-px flex-1 bg-white/10" />
            <span className="text-sm text-gray-500">
              or continue with
            </span>
            <div className="h-px flex-1 bg-white/10" />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <button
              type="button"
              className="rounded-xl border border-white/10 bg-white/[0.03] py-3 font-medium transition-all duration-300 hover:border-violet-500/40 hover:bg-white/[0.05]"
            >
              Google
            </button>

            <button
              type="button"
              className="rounded-xl border border-white/10 bg-white/[0.03] py-3 font-medium transition-all duration-300 hover:border-violet-500/40 hover:bg-white/[0.05]"
            >
              GitHub
            </button>
          </div>

          <p className="text-center text-sm text-gray-400">
            Don't have an account?{" "}
            <Link
              to="/register"
              className="font-medium text-violet-400 hover:text-violet-300"
            >
              Sign up
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}
