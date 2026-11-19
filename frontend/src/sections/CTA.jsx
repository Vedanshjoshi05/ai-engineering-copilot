
import { ArrowRight, Sparkles } from 'lucide-react';
import { FaGithub } from 'react-icons/fa';

function CTA() {
  return (
    <section id="connect" className="px-6 py-24 lg:px-10">
      <div className="mx-auto max-w-6xl overflow-hidden rounded-[2rem] bg-slate-900 px-7 py-16 text-center sm:px-12">

        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-500/20 text-blue-400">
          <Sparkles size={27} />
        </div>

        <h2 className="mx-auto mt-7 max-w-3xl text-3xl font-semibold tracking-tight text-white sm:text-5xl">
          Ready to understand your
          <span className="text-blue-400"> codebase?</span>
        </h2>

        <p className="mx-auto mt-6 max-w-xl leading-7 text-slate-400">
          Connect your GitHub repository and start exploring
          your code with Nexora.
        </p>

        <a
          href="https://github.com"
          target="_blank"
          rel="noreferrer"
          className="mx-auto mt-9 inline-flex items-center gap-3 rounded-full bg-white px-7 py-4 text-sm font-semibold text-slate-900 transition hover:-translate-y-1 hover:bg-blue-50"
        >
          <FaGithub size={19} />
          Get started with GitHub
          <ArrowRight size={17} />
        </a>

      </div>
    </section>
  );
}

export default CTA;
