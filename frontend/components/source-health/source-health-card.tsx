import type { SourceHealth } from "@/types/source";
import { HealthBadge } from "./health-badge";

interface SourceHealthCardProps {
  source: SourceHealth;
}

export function SourceHealthCard({ source }: SourceHealthCardProps) {
  return (
    <article className="rounded-xl border bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold capitalize">{source.source}</h2>

          <p className="mt-1 text-sm text-gray-500">
            Crawl #{source.latest_crawl_id}
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

      {source.latest_error_message && (
        <div className="mt-4 rounded-lg bg-red-50 p-4 text-sm text-red-700">
          {source.latest_error_message}
        </div>
      )}
    </article>
  );
}
