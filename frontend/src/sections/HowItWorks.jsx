import { Database, MessageSquareText, ArrowRight } from 'lucide-react';
import { FaGithub } from 'react-icons/fa';

const steps=[
    {
        number:'01',
        icon:FaGithub,
        title:'Connect your repository',
        description:'Simply provide your Github repository URL. Nexora collects the relevant source files and project information.',
    },
    {
        number:'02',
        icon:Database,
        title:'Index your codebase',
        description:'Source code is divided into smaller chunks, converted into embeddings, and indexed for semantic search.',
    },
    {
        number:'03',
        icon:MessageSquareText,
        title:'Ask and understand',
        description:'Ask questions in natural language and receive AI-generated answers based on retrieved repository code.',
    },
   

];


function HowItWorks() {
  return (
    <section id="how-it-works" className="bg-white px-6 py-24 lg:px-10">
      <div className="mx-auto max-w-7xl">

        <div className="mx-auto max-w-2xl text-center">
          <span className="text-sm font-semibold uppercase tracking-[0.2em] text-blue-600">
            Simple workflow
          </span>

          <h2 className="mt-4 text-3xl font-semibold tracking-tight text-slate-900 sm:text-5xl">
            From repository to
            <span className="text-blue-600"> understanding.</span>
          </h2>

          <p className="mt-5 leading-7 text-slate-500">
            Get started with your codebase in three simple steps.
            No complicated setup required.
          </p>
        </div>

        <div className="mt-16 grid gap-6 md:grid-cols-3">
          {steps.map((step) => {
            const Icon = step.icon;

            return (
              <div
                key={step.number}
                className="group rounded-3xl border border-slate-200 bg-[#fbfcfb] p-8 transition duration-300 hover:-translate-y-2 hover:border-blue-200 hover:shadow-xl hover:shadow-blue-900/5"
              >
                <div className="flex items-center justify-between">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-50 text-blue-600 transition group-hover:bg-blue-600 group-hover:text-white">
                    <Icon size={25} />
                  </div>

                  <span className="text-4xl font-semibold text-slate-100">
                    {step.number}
                  </span>
                </div>

                <h3 className="mt-8 text-xl font-semibold text-slate-900">
                  {step.title}
                </h3>

                <p className="mt-4 text-sm leading-7 text-slate-500">
                  {step.description}
                </p>

                <div className="mt-7 flex items-center gap-2 text-sm font-semibold text-blue-600">
                  Explore
                  <ArrowRight
                    size={16}
                    className="transition group-hover:translate-x-1"
                  />
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}

export default HowItWorks;