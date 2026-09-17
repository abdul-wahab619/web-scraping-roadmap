import type { CrawlRun } from "@/types/source";
import { StatusBadge } from "./status-badge";

interface CrawlHistoryProps {
  crawls: CrawlRun[];
}

function formatDate(value: string | null) {
  if (!value) {
    return "N/A";
  }

  return new Date(value).toLocaleString();
}

export function CrawlHistory({ crawls }: CrawlHistoryProps) {
  return (
    <section className="mt-8">
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Recent Crawl History</h2>

        <p className="mt-1 text-sm text-gray-500">
          Recent crawl runs for this source.
        </p>
      </div>

      <div className="overflow-hidden rounded-xl border bg-white">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-gray-50">
              <tr>
                <th className="px-4 py-3 font-medium">Crawl</th>

                <th className="px-4 py-3 font-medium">Status</th>

                <th className="px-4 py-3 font-medium">Items</th>

                <th className="px-4 py-3 font-medium">Requests</th>

                <th className="px-4 py-3 font-medium">Retries</th>

                <th className="px-4 py-3 font-medium">Duration</th>

                <th className="px-4 py-3 font-medium">Started</th>
              </tr>
            </thead>

            <tbody>
              {crawls.map((crawl) => (
                <tr key={crawl.id} className="border-b last:border-b-0">
                  <td className="px-4 py-3 font-medium">#{crawl.id}</td>

                  <td className="px-4 py-3">
                    <StatusBadge status={crawl.status} />
                  </td>

                  <td className="px-4 py-3">{crawl.items_found}</td>

                  <td className="px-4 py-3">{crawl.requests}</td>

                  <td className="px-4 py-3">{crawl.retries}</td>
                  <td className="px-4 py-3">
                    {crawl.finished_at
                      ? (
                          (new Date(crawl.finished_at).getTime() -
                            new Date(crawl.started_at).getTime()) /
                          1000
                        ).toFixed(2)
                      : "Running"}
                    s
                  </td>

                  <td className="px-4 py-3 whitespace-nowrap">
                    {formatDate(crawl.started_at)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
