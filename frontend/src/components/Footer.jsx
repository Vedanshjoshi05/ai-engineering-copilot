
import { Code2} from 'lucide-react';
import { FaGithub } from 'react-icons/fa';

function Footer() {
  return (
    <footer id="about" className="border-t border-slate-200 bg-white px-6 py-10 lg:px-10">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-6 sm:flex-row">

        <a href="#" className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600 text-white">
            <Code2 size={20} />
          </div>

          <span className="text-xl font-bold text-slate-900">
            nexora<span className="text-blue-600">.</span>
          </span>
        </a>

        <p className="text-center text-sm text-slate-500">
          Making complex codebases easier to understand.
        </p>

        <a
          href="https://github.com"
          target="_blank"
          rel="noreferrer"
          aria-label="GitHub"
          className="text-slate-500 transition hover:text-blue-600"
        >
          <FaGithub size={22} />
        </a>
      </div>

      <div className="mx-auto mt-8 max-w-7xl border-t border-slate-100 pt-6 text-center text-xs text-slate-400">
        © {new Date().getFullYear()} Nexora. Built for developers.
      </div>
    </footer>
  );
}

export default Footer;
