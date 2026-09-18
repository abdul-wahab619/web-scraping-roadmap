import type { CrawlRun } from "@/types/source";

interface LatestCrawlSummaryProps {
  crawl: CrawlRun;
}

export function LatestCrawlSummary({ crawl }: LatestCrawlSummaryProps) {
  const duration = crawl.finished_at
    ? (
        (new Date(crawl.finished_at).getTime() -
          new Date(crawl.started_at).getTime()) /
        1000
      ).toFixed(2)
    : null;

  const metrics = [
    {
      label: "Items Found",
      value: crawl.items_found,
    },
    {
      label: "Items Dropped",
      value: crawl.items_dropped,
    },
    {
      label: "Requests",
      value: crawl.requests,
    },
    {
      label: "Responses",
      value: crawl.responses,
    },
    {
      label: "Retries",
      value: crawl.retries,
    },
    {
      label: "HTTP Errors",
      value: crawl.http_errors,
    },
    {
      label: "Exceptions",
      value: crawl.spider_exceptions,
    },
    {
      label: "Duration",
      value: duration ? `${duration}s` : "Running",
    },
  ];

  return (
    <section className="mt-8">
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Latest Crawl</h2>

        <p className="mt-1 text-sm text-gray-500">
          Operational metrics from the latest crawl run.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric) => (
          <div
            key={metric.label}
            className="rounded-xl border bg-white p-5 shadow-sm"
          >
            <p className="text-sm text-gray-500">{metric.label}</p>

            <p className="mt-2 text-2xl font-semibold">{metric.value}</p>
          </div>
        ))}
      </div>

      {crawl.error_message && (
        <div className="mt-4 rounded-xl border border-red-200 bg-red-50 p-5">
          <p className="text-sm font-semibold text-red-800">Crawl Error</p>

          <p className="mt-1 text-sm text-red-700">{crawl.error_message}</p>
        </div>
      )}
    </section>
  );
}
