import { useState } from "react";
import { Bot, Menu, X } from "lucide-react";
import { Link } from "react-router-dom";

function Navbar() {
  const [open, setOpen] = useState(false);

  const navLinks = [
    { name: "Features", href: "#features" },
    { name: "How It Works", href: "#how-it-works" },
    { name: "Pricing", href: "#pricing" },
    { name: "Testimonials", href: "#testimonials" },
    { name: "FAQ", href: "#faq" },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-white/5  bg-[#000204] text-white backdrop-blur-md">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 md:px-6">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 text-xl font-bold">
          <div className="rounded-md bg-gradient-to-r from-[#5133CA] to-[#B72CFF] p-2">
            <Bot size={24} />
          </div>
          <span>InterviewAI</span>
        </Link>

        <div className="hidden items-center gap-8 text-sm text-white/70 md:flex">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className="transition hover:text-white"
            >
              {link.name}
            </a>
          ))}
        </div>

        <div className="hidden items-center gap-3 md:flex">
          <Link
            to="/login"
            className="rounded-md border border-white/20 px-5 py-2.5 text-sm text-gray-300 transition hover:border-white/40 hover:text-white"
          >
            Login
          </Link>

          <Link
            to="/register"
            className="rounded-md bg-gradient-to-r from-[#5133CA] to-[#B72CFF] px-5 py-2.5 text-sm font-medium text-white transition hover:opacity-90"
          >
            Get Started
          </Link>
        </div>

        <button
          onClick={() => setOpen(!open)}
          className="rounded-md border border-white/10 p-2 md:hidden"
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </nav>
      {open && (
        <div className="border-t border-white/10 bg-[#000204] px-5 py-5 md:hidden">
          <div className="flex flex-col gap-4 text-sm text-white/80">
            {navLinks.map((link) => (
              <a
                key={link.name}
                href={link.href}
                onClick={() => setOpen(false)}
                className="transition hover:text-white"
              >
                {link.name}
              </a>
            ))}
          </div>

          <div className="mt-6 flex flex-col gap-3">
            <Link
              to="/login"
              onClick={() => setOpen(false)}
              className="rounded-md border border-white/20 px-5 py-2.5 text-center text-sm text-gray-300"
            >
              Login
            </Link>

            <Link
              to="/register"
              onClick={() => setOpen(false)}
              className="rounded-md bg-gradient-to-r from-[#5133CA] to-[#B72CFF] px-5 py-2.5 text-center text-sm font-medium text-white"
            >
              Get Started
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}

export default Navbar;