import type { SourceHealth } from "@/types/source";
import { HealthBadge } from "./health-badge";
import Link from "next/link";
interface SourceHealthCardProps {
  source: SourceHealth;
}

function formatDate(value: string | null) {
  if (!value) {
    return "N/A";
  }

  return new Date(value).toLocaleString();
}

export function SourceHealthCard({ source }: SourceHealthCardProps) {
  let healthMessage = "Source is operating normally.";

  if (source.health.toUpperCase() === "WARNING") {
    if (
      source.avg_items_found !== null &&
      source.percentage_of_average !== null &&
      source.latest_items_found < source.avg_items_found * 0.5
    ) {
      healthMessage =
        `Latest crawl returned ${source.latest_items_found} items, ` +
        `which is significantly below the historical average of ` +
        `${source.avg_items_found.toFixed(1)}.`;
    } else if (source.latest_items_dropped > 0) {
      healthMessage = `Latest crawl dropped ${source.latest_items_dropped} item(s).`;
    } else {
      healthMessage =
        "Source completed its latest crawl but requires attention.";
    }
  }

  if (source.health.toUpperCase() === "FAILED") {
    healthMessage = source.latest_error_message ?? "The latest crawl failed.";
  }

  return (
    <article className="rounded-xl border bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <Link
            href={`/sources/${encodeURIComponent(source.source)}`}
            className="text-xl font-semibold capitalize hover:underline"
          >
            {source.source}
          </Link>

          <p className="mt-1 text-sm text-gray-500">
            Latest crawl #{source.latest_crawl_id}
          </p>
        </div>

        <HealthBadge health={source.health} />
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div>
          <p className="text-sm text-gray-500">Items</p>
          <p className="mt-1 text-2xl font-semibold">
            {source.latest_items_found}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Avg Items</p>
          <p className="mt-1 text-2xl font-semibold">
            {source.avg_items_found ?? "N/A"}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Duration</p>
          <p className="mt-1 text-2xl font-semibold">
            {source.latest_duration_seconds?.toFixed(2) ?? "N/A"}s
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Failed Crawls</p>
          <p className="mt-1 text-2xl font-semibold">{source.failed_crawls}</p>
        </div>
      </div>

      <div className="mt-6 grid gap-4 border-t pt-4 sm:grid-cols-2">
        <div>
          <p className="text-xs text-gray-500">Last Successful Crawl</p>

          <p className="mt-1 text-sm font-medium">
            {formatDate(source.last_successful_crawl)}
          </p>
        </div>

        <div>
          <p className="text-xs text-gray-500">Latest Finished</p>

          <p className="mt-1 text-sm font-medium">
            {formatDate(source.latest_finished_at)}
          </p>
        </div>
      </div>

      <div className="mt-6 grid gap-4 border-t pt-4 sm:grid-cols-3">
        <div>
          <p className="text-xs text-gray-500">Requests</p>
          <p className="font-medium">{source.latest_requests}</p>
        </div>

        <div>
          <p className="text-xs text-gray-500">Responses</p>
          <p className="font-medium">{source.latest_responses}</p>
        </div>

        <div>
          <p className="text-xs text-gray-500">Retries</p>
          <p className="font-medium">{source.latest_retries}</p>
        </div>
      </div>

      <div className="mt-6 rounded-lg bg-gray-50 p-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
          Health Explanation
        </p>

        <p className="mt-1 text-sm text-gray-700">{healthMessage}</p>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-3 border-t pt-6 sm:grid-cols-4">
        <div className="rounded-lg bg-gray-50 p-3">
          <p className="text-xs text-gray-500">Dropped</p>

          <p className="mt-1 text-lg font-semibold">
            {source.latest_items_dropped}
          </p>
        </div>

        <div className="rounded-lg bg-gray-50 p-3">
          <p className="text-xs text-gray-500">Retries</p>

          <p className="mt-1 text-lg font-semibold">{source.latest_retries}</p>
        </div>

        <div className="rounded-lg bg-gray-50 p-3">
          <p className="text-xs text-gray-500">HTTP Errors</p>

          <p className="mt-1 text-lg font-semibold">
            {source.latest_http_errors}
          </p>
        </div>

        <div className="rounded-lg bg-gray-50 p-3">
          <p className="text-xs text-gray-500">Exceptions</p>

          <p className="mt-1 text-lg font-semibold">
            {source.latest_spider_exceptions}
          </p>
        </div>
      </div>

      {source.latest_error_message && (
        <div className="mt-4 rounded-lg bg-red-50 p-4 text-sm text-red-700">
          {source.latest_error_message}
        </div>
      )}
    </article>
  );
}
