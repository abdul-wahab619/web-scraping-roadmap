import { getSourceHealth, getSourceCrawls } from "@/lib/api";
import { SourceHealthCard } from "@/components/source-health/source-health-card";
import { CrawlHistory } from "@/components/source-health/crawl-history";
import { DashboardStats } from "@/components/source-health/dashboard-stats";
import { EmptyState } from "@/components/source-health/empty-state";
import { RefreshButton } from "@/components/source-health/refresh-button";
import { AutoRefresh } from "@/components/source-health/auto-refresh";

export default async function Home() {
  const sources = await getSourceHealth();

  const crawlHistory = await Promise.all(
    sources.map(async (source) => ({
      source: source.source,
      crawls: await getSourceCrawls(source.source, 10),
    })),
  );

  return (
    <main className="min-h-screen bg-gray-50 px-6 py-10 text-slate-800">
      <AutoRefresh />
      <div className="mx-auto max-w-6xl">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Source Health</h1>

            <p className="mt-2 text-gray-600">
              Monitor the health and performance of your scraping sources.
            </p>
          </div>

          <RefreshButton />
        </div>
        <DashboardStats sources={sources} />
        {sources.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="mt-8 grid gap-6">
            {sources.map((source) => (
              <SourceHealthCard key={source.source} source={source} />
            ))}
          </div>
        )}

        {crawlHistory.map((history) => (
          <CrawlHistory key={history.source} crawls={history.crawls} />
        ))}
      </div>
    </main>
  );
}
