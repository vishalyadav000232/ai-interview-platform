import BackHome from "../../../../components/ui/BackHome";
import { Logo } from "../../../../components/ui/Logo";
import { LoginForm } from "../../components/LoginForm";
import { LoginPreview } from "../../components/LoginPreviews";


export const LoginPage = () => {
  return (
    <section className="min-h-screen overflow-hidden bg-[#000204] text-white">
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-6 lg:px-8">

        {/* Header */}
        <header className="flex h-20 shrink-0 items-center justify-between">
          <Logo />
          <BackHome />
        </header>

        {/* Main */}
        <main className="flex flex-1 items-center py-8">
          <div className="grid w-full grid-cols-1 items-center gap-16 lg:grid-cols-[420px_minmax(0,1fr)] lg:gap-20">

            {/* Login Form */}
            <div className="flex justify-center lg:justify-start">
              <div className="w-full max-w-[420px]">
                <LoginForm />
              </div>
            </div>

            {/* Right Preview */}
            <div className="hidden justify-center lg:flex">
              <div className="w-full max-w-[560px]">
                <LoginPreview />
              </div>
            </div>

          </div>
        </main>

      </div>
    </section>
  );
};
