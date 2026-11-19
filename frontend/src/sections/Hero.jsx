import {
  ArrowRight,
  Sparkles,
  Search,
  FileCode2,
  MessageSquare,
  CheckCircle2
} from 'lucide-react';

import { FaGithub } from 'react-icons/fa';

function Hero() {
  return (
    <section className="relative overflow-hidden px-6 pb-24 pt-16 lg:px-10 lg:pt-24">

      {/* Background decoration */}
      <div className="pointer-events-none absolute -left-40 top-10 h-96 w-96 rounded-full bg-teal-200/30 blur-3xl" />
      <div className="pointer-events-none absolute -right-40 top-20 h-96 w-96 rounded-full bg-blue-200/30 blur-3xl" />

      <div className="relative mx-auto max-w-5xl text-center">

        {/* Label */}
        <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-white/70 px-4 py-2 text-sm font-medium text-blue-700 shadow-sm">
          <Sparkles size={15} />
          AI-powered software engineering
        </div>

        {/* Heading */}
        <h1 className="mx-auto max-w-4xl text-5xl font-semibold leading-[1.12] tracking-tight text-slate-900 sm:text-6xl lg:text-7xl">
          Your entire codebase,
          <span className="block text-blue-600">
            understood by AI.
          </span>
        </h1>

        {/* Description */}
        <p className="mx-auto mt-7 max-w-2xl text-base leading-8 text-slate-600 sm:text-lg">
          Connect your GitHub repository and let Nexora help you
          understand code, explore project structure, and get
          answers to your development questions.
        </p>

        {/* CTA */}
        <div className="mt-9 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a
            href="#connect"
            className="group flex items-center gap-3 rounded-full bg-slate-900 px-7 py-4 text-sm font-semibold text-white shadow-lg transition hover:-translate-y-1 hover:bg-blue-600"
          >
            Explore your repository
            <ArrowRight size={18} className="transition group-hover:translate-x-1" />
          </a>

          <a
            href="#how-it-works"
            className="rounded-full border border-slate-300 bg-white/70 px-7 py-4 text-sm font-semibold text-slate-700 transition hover:border-blue-400 hover:text-blue-600"
          >
            See how it works
          </a>
        </div>

        {/* Product preview */}
        <div className="relative mx-auto mt-20 max-w-4xl">

          <div className="absolute -inset-4 rounded-[2rem] bg-gradient-to-r from-teal-200/40 via-blue-200/30 to-orange-100/40 blur-2xl" />

          <div className="relative overflow-hidden rounded-2xl border border-slate-200 bg-white text-left shadow-2xl shadow-slate-900/10">

            {/* Window header */}
            <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded-full bg-red-400" />
                <span className="h-3 w-3 rounded-full bg-yellow-400" />
                <span className="h-3 w-3 rounded-full bg-green-400" />
              </div>

              <span className="text-xs font-medium text-slate-400">
                Nexora AI Workspace
              </span>

              <FaGithub size={18} className="text-slate-500" />
            </div>

            {/* Preview content */}
            <div className="grid md:grid-cols-[1fr_1.5fr]">

              {/* Repository panel */}
              <div className="border-b border-slate-100 p-6 md:border-b-0 md:border-r">
                <div className="mb-5 flex items-center gap-2">
                  <FaGithub size={19} />
                  <span className="font-semibold text-slate-800">
                    Repository
                  </span>
                </div>

                <div className="rounded-xl bg-slate-50 p-4">
                  <div className="flex items-center gap-2 text-sm font-semibold text-slate-800">
                    <FileCode2 size={17} className="text-blue-600" />
                    sample-project
                  </div>

                  <div className="mt-4 space-y-3 text-sm text-slate-500">
                    <div className="flex items-center gap-2">
                      <FileCode2 size={15} /> src/
                    </div>
                    <div className="flex items-center gap-2 pl-5">
                      <FileCode2 size={15} /> main.py
                    </div>
                    <div className="flex items-center gap-2 pl-5">
                      <FileCode2 size={15} /> services.py
                    </div>
                    <div className="flex items-center gap-2">
                      <FileCode2 size={15} /> README.md
                    </div>
                  </div>
                </div>

                <div className="mt-5 flex items-center gap-2 text-xs font-medium text-green-600">
                  <CheckCircle2 size={15} />
                  Repository indexed
                </div>
              </div>

              {/* AI chat panel */}
              <div className="p-6">
                <div className="mb-6 flex items-center gap-2">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-100 text-blue-600">
                    <Sparkles size={17} />
                  </div>
                  <span className="font-semibold text-slate-800">
                    Ask Nexora
                  </span>
                </div>

                <div className="ml-auto max-w-[90%] rounded-xl bg-blue-600 p-4 text-sm text-white">
                  How does the application handle API requests?
                </div>

                <div className="mt-5 flex gap-3">
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
                    <MessageSquare size={17} />
                  </div>

                  <div>
                    <p className="text-sm font-semibold text-slate-800">
                      Nexora AI
                    </p>
                    <p className="mt-2 text-sm leading-6 text-slate-500">
                      The application handles API requests through its
                      service layer. I found relevant implementation
                      details in the repository source files.
                    </p>
                    <div className="mt-3 flex items-center gap-2 text-xs text-blue-600">
                      <Search size={13} />
                      Source: src/services.py
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <p className="mt-5 text-center text-xs text-slate-400">
            An illustrative preview of the Nexora experience
          </p>
        </div>
      </div>
    </section>
  );
}

export default Hero;
