
import { Code2, Menu } from 'lucide-react';
import { FaGithub } from 'react-icons/fa';

function Navbar() {
  return (
    <nav className="relative z-20 mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-10">

      {/* Logo */}
      <a href="#" className="flex items-center gap-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white">
          <Code2 size={23} />
        </div>

        <span className="text-2xl font-bold tracking-tight text-slate-900">
          nexora<span className="text-blue-600">.</span>
        </span>
      </a>

      {/* Navigation links */}
      <div className="hidden items-center gap-9 text-sm font-medium text-slate-600 md:flex">
        <a href="#features" className="transition hover:text-blue-600">
          Features
        </a>
        <a href="#how-it-works" className="transition hover:text-blue-600">
          How it works
        </a>
        <a href="#about" className="transition hover:text-blue-600">
          About
        </a>
      </div>

      {/* Right actions */}
      <div className="flex items-center gap-3">
        <a
          href="https://github.com"
          target="_blank"
          rel="noreferrer"
          className="hidden items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 transition hover:border-blue-300 sm:flex"
        >
          <FaGithub size={17} />
          GitHub
        </a>

        <a
          href="#connect"
          className="rounded-full bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-600"
        >
          Get started
        </a>

        <button className="rounded-lg p-2 text-slate-700 md:hidden" aria-label="Open navigation menu">
          <Menu size={23} />
        </button>
      </div>

    </nav>
  );
}

export default Navbar;
