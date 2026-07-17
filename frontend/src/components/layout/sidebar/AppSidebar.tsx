import { ChevronDown, Sparkles } from "lucide-react";

import { useAuthStore } from "../../../features/auth/store/auth.store";

import {
  accountSidebarSection,
  mainSidebarSection,
} from "./sidebar.config";

import { SidebarSection } from "./SidebarSection";

export function AppSidebar() {
  const user = useAuthStore((state) => state.user);

  const userEmail = user?.email ?? "user@example.com";
  const userName = user?.first_name ?? "Vishal Yadav";

  const userInitial = userName
    .trim()
    .charAt(0)
    .toUpperCase() || "U";

  return (
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-72 border-r border-white/10 bg-[#080a0f] lg:flex lg:flex-col">
      <div className="flex h-20 shrink-0 items-center border-b border-white/10 px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-600 text-white">
            <Sparkles
              className="h-5 w-5"
              strokeWidth={2}
              aria-hidden="true"
            />
          </div>

          <div>
            <p className="text-base font-semibold text-white">
              InterviewAI
            </p>

            <p className="text-xs text-slate-500">
              Your AI Interview Coach
            </p>
          </div>
        </div>
      </div>

      <div className="flex-1 space-y-7 overflow-y-auto px-4 py-6">
        <SidebarSection section={mainSidebarSection} />

        <SidebarSection section={accountSidebarSection} />

        <div className="rounded-2xl border border-violet-500/20 bg-violet-500/10 p-4">
          <div className="mb-3 flex h-9 w-9 items-center justify-center rounded-lg bg-violet-500/20 text-violet-300">
            <Sparkles
              className="h-4 w-4"
              aria-hidden="true"
            />
          </div>

          <h3 className="text-sm font-semibold text-white">
            Upgrade to Pro
          </h3>

          <p className="mt-1 text-xs leading-5 text-slate-400">
            Unlock unlimited mock interviews and advanced AI feedback.
          </p>

          <button
            type="button"
            className="mt-4 w-full rounded-lg bg-violet-600 px-3 py-2 text-sm font-semibold text-white transition-colors hover:bg-violet-500"
          >
            View plans
          </button>
        </div>
      </div>

      <div className="shrink-0 border-t border-white/10 p-4">
        <button
          type="button"
          className="flex w-full items-center gap-3 rounded-xl p-2 text-left transition-colors hover:bg-white/5"
        >
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-violet-600 text-sm font-semibold text-white">
            {userInitial}
          </div>

          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium text-white">
              {userName}
            </p>

            <p className="truncate text-xs text-slate-500">
              {userEmail}
            </p>
          </div>

          <ChevronDown
            className="h-4 w-4 shrink-0 text-slate-500"
            aria-hidden="true"
          />
        </button>
      </div>
    </aside>
  );
}
