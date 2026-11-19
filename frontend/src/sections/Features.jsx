
import {
  SearchCode,
  Network,
  Bug,
  Code2,
  FileText,
  Zap,
} from 'lucide-react';

const features = [
  {
    icon: SearchCode,
    title: 'Repository understanding',
    description:
      'Explore source files and ask questions about how your codebase works.',
    status: 'Available',
  },
  {
    icon: Network,
    title: 'Architecture analysis',
    description:
      'Understand modules, components, and relationships across your project.',
    status: 'In development',
  },
  {
    icon: Bug,
    title: 'Bug detection',
    description:
      'Identify potential bugs and get recommendations to improve code quality.',
    status: 'In development',
  },
  {
    icon: Code2,
    title: 'Code review',
    description:
      'Explore potential improvements and understand problematic code sections.',
    status: 'In development',
  },
  {
    icon: FileText,
    title: 'Code documentation',
    description:
      'Make complex code easier to understand with clear explanations.',
    status: 'Planned',
  },
  {
    icon: Zap,
    title: 'Developer productivity',
    description:
      'Spend less time navigating unfamiliar repositories and more time building.',
    status: 'Vision',
  },
];

function Features() {
  return (
    <section id="features" className="bg-[#f6faf9] px-6 py-24 lg:px-10">
      <div className="mx-auto max-w-7xl">

        <div className="max-w-2xl">
          <span className="text-sm font-semibold uppercase tracking-[0.2em] text-blue-600">
            What Nexora offers
          </span>

          <h2 className="mt-4 text-3xl font-semibold tracking-tight text-slate-900 sm:text-5xl">
            Everything you need to
            <span className="text-blue-600"> understand code.</span>
          </h2>

          <p className="mt-5 leading-7 text-slate-500">
            A growing set of AI-powered tools designed to simplify
            software development and repository exploration.
          </p>
        </div>

        <div className="mt-14 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => {
            const Icon = feature.icon;

            return (
              <div
                key={feature.title}
                className="rounded-2xl border border-slate-200 bg-white p-7 transition duration-300 hover:-translate-y-1 hover:border-blue-200 hover:shadow-lg hover:shadow-slate-900/5"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                  <Icon size={23} />
                </div>

                <div className="mt-6 flex flex-wrap items-center justify-between gap-2">
                  <h3 className="text-lg font-semibold text-slate-900">
                    {feature.title}
                  </h3>

                  <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[10px] font-medium text-slate-500">
                    {feature.status}
                  </span>
                </div>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}

export default Features;
