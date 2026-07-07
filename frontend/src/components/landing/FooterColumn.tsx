import { Link } from "react-router-dom";



type FooterColumnProps = {
  title: string;
  links: string[];
};

export const FooterColumn = ({ title, links }: FooterColumnProps) => {
  return (
    <div>
      <h3 className="text-sm font-semibold text-white">{title}</h3>

      <ul className="mt-5 space-y-3">
        {links.map((link) => (
          <li key={link}>
            <Link
              to="#"
              className="text-sm text-gray-400 transition hover:text-violet-400"
            >
              {link}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};