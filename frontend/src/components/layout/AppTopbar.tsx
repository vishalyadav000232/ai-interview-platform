import { Bell, Menu, Search } from "lucide-react";

import { useAuthStore } from "../../features/auth/store/auth.store";

export function AppTopbar() {
  const user = useAuthStore((state) => state.user);

  const userName = user?.first_name ?? "Vishal";

  const userInitial =
    userName.trim().charAt(0).toUpperCase() || "U";

  return (
    <header className="flex items-start justify-between gap-6 px-6 pb-5 pt-7 lg:px-8">
      <div className="flex min-w-0 items-start gap-3">
        <button
          type="button"
          aria-label="Open sidebar"
          className="mt-1 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-white/10 text-slate-400 transition-colors hover:bg-white/5 hover:text-white lg:hidden"
        >
          <Menu className="h-5 w-5" aria-hidden="true" />
        </button>

        <div className="min-w-0">
          <h1 className="truncate text-2xl font-semibold tracking-tight text-white">
            Good morning, {userName}! 👋
          </h1>

          <p className="mt-1 text-sm text-slate-400">
            Let&apos;s continue your{" "}
            <span className="font-medium text-violet-400">
              Backend Developer
            </span>{" "}
            preparation.
          </p>
        </div>
      </div>

      <div className="flex shrink-0 items-center gap-4">
        <div className="relative hidden w-[410px] xl:block">
          <Search
            className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500"
            aria-hidden="true"
          />

          <input
            type="search"
            placeholder="Search anything..."
            className="h-11 w-full rounded-xl border border-white/10 bg-[#0a0d14] pl-12 pr-4 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-violet-500/50"
          />
        </div>

        <button
          type="button"
          aria-label="Search"
          className="flex h-11 w-11 items-center justify-center rounded-xl border border-white/10 text-slate-400 transition hover:bg-white/5 hover:text-white xl:hidden"
        >
          <Search className="h-5 w-5" aria-hidden="true" />
        </button>

        <button
          type="button"
          aria-label="Notifications"
          className="relative flex h-11 w-11 items-center justify-center text-slate-300 transition hover:text-white"
        >
          <Bell className="h-6 w-6" strokeWidth={1.8} aria-hidden="true" />

          <span className="absolute right-1 top-0 flex h-4 min-w-4 items-center justify-center rounded-full bg-violet-600 px-1 text-[10px] font-semibold text-white">
            3
          </span>
        </button>

        <button
          type="button"
          aria-label="Open profile menu"
          className="flex h-11 w-11 items-center justify-center rounded-full border border-white/20 bg-violet-600 text-sm font-semibold text-white transition hover:border-violet-400"
        >
          {userInitial}
        </button>
      </div>
    </header>
  );
}
