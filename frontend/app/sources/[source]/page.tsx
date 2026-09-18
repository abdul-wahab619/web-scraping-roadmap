import { getSourceCrawls, getSourceHealthBySource } from "@/lib/api";
import { notFound } from "next/navigation";
import Link from "next/link";
import { SourceHealthCard } from "@/components/source-health/source-health-card";
import { CrawlHistory } from "@/components/source-health/crawl-history";
import { LatestCrawlSummary } from "@/components/source-health/latest-crawl-summary";

interface SourcePageProps {
  params: Promise<{
    source: string;
  }>;
}

export default async function SourcePage({ params }: SourcePageProps) {
  const { source } = await params;

  let health;

  try {
    health = await getSourceHealthBySource(source);
  } catch {
    notFound();
  }

  const crawls = await getSourceCrawls(source, 20);

  return (
    <main className="min-h-screen bg-gray-50 px-6 py-10 text-slate-800">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/"
          className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900"
        >
          ← Back to Dashboard
        </Link>
        <div>
          <p className="text-sm text-gray-500">Source</p>

          <h1 className="mt-1 text-3xl font-bold tracking-tight capitalize">
            {source}
          </h1>

          <p className="mt-2 text-gray-600">
            Detailed health and crawl history for this source.
          </p>
        </div>

        <div className="mt-8">
          <SourceHealthCard source={health} />
        </div>
        <LatestCrawlSummary crawl={crawls[0]} />

        <CrawlHistory crawls={crawls} />
      </div>
    </main>
  );
}
