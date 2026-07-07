import { ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";

const BackHome = () => {
  return (
    <Link
      to="/"
      className="group inline-flex items-center gap-2 text-sm font-medium text-gray-300 transition-colors duration-300 hover:text-white"
    >
      <ArrowLeft className="h-5 w-5 text-[#8E51FF] transition-transform duration-300 group-hover:-translate-x-1" />

      <span>Back to Home</span>
    </Link>
  );
};

export default BackHome;