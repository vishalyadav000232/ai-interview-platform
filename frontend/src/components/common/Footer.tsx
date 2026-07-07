
import { BsTwitter, BsYoutube } from "react-icons/bs";
import { FaGithub } from "react-icons/fa";
import { LiaLinkedin } from "react-icons/lia";
import { Link } from "react-router-dom";
import { FooterColumn } from "../landing/FooterColumn";

const productLinks = [
  "Features",
  "Mock Interview",
  "Resume ATS",
  "Dashboard",
  "Pricing",
];

const resourceLinks = ["FAQ", "Blog", "Documentation", "Interview Guide"];

const companyLinks = ["About", "Contact", "Careers", "Support"];

const legalLinks = ["Privacy Policy", "Terms & Conditions", "Cookie Policy"];

const Footer = () => {
  return (
    <footer className="bg-[#000204] text-white">
      <div className="mx-auto max-w-7xl px-5 py-16">
        <div className="grid gap-12 border-t border-white/10 pt-12 md:grid-cols-2 lg:grid-cols-5">
         
          <div className="lg:col-span-2">
            <Link to="/" className="text-2xl font-bold">
              AI<span className="text-violet-500">Interview</span>
            </Link>

            <p className="mt-5 max-w-sm text-sm leading-6 text-gray-400">
              Ace your interviews with AI-powered mock interviews, resume
              analysis, coding practice, and personalized feedback.
            </p>

            <div className="mt-6 flex gap-4">
              <a
                href="#"
                className="rounded-full border border-white/10 p-2 text-gray-400 transition hover:border-violet-500 hover:text-violet-400"
              >
                <FaGithub size={18} />
              </a>

              <a
                href="#"
                className="rounded-full border border-white/10 p-2 text-gray-400 transition hover:border-violet-500 hover:text-violet-400"
              >
                <LiaLinkedin size={18} />
              </a>

              <a
                href="#"
                className="rounded-full border border-white/10 p-2 text-gray-400 transition hover:border-violet-500 hover:text-violet-400"
              >
                <BsYoutube size={18} />
              </a>

              <a
                href="#"
                className="rounded-full border border-white/10 p-2 text-gray-400 transition hover:border-violet-500 hover:text-violet-400"
              >
                <BsTwitter size={18} />
              </a>
            </div>
          </div>

    
          <FooterColumn title="Product" links={productLinks} />

      
          <FooterColumn title="Resources" links={resourceLinks} />


          <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-1">
            <FooterColumn title="Company" links={companyLinks} />
            <FooterColumn title="Legal" links={legalLinks} />
          </div>
        </div>

        <div className="mt-12 flex flex-col gap-4 border-t border-white/10 pt-6 text-sm text-gray-500 md:flex-row md:items-center md:justify-between">
          <p>© 2026 AI Interview Platform. All rights reserved.</p>
          <p>
            Built with <span className="text-violet-500">❤️</span> by CodeYatra
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
