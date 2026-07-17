import { Outlet } from "react-router-dom";
import { AppTopbar } from "./AppTopbar";
import { AppSidebar } from "./sidebar/AppSidebar";

export function AppLayout() {
  return (
    <div className="min-h-screen bg-[#05070c] text-white">
      <AppSidebar />

      <div className="min-h-screen lg:pl-72">
        <AppTopbar />

        <main className="px-6 pb-8 lg:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
