import type { SourceHealth, CrawlRun } from "@/types/source";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  throw new Error("NEXT_PUBLIC_API_URL is not defined");
}

export async function getSourceHealth(): Promise<SourceHealth[]> {
  const response = await fetch(`${API_URL}/sources/health`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch source health");
  }

  return response.json();
}

export async function getSourceHealthBySource(
  source: string,
): Promise<SourceHealth> {
  const response = await fetch(
    `${API_URL}/sources/health/${encodeURIComponent(source)}`,
    {
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch health for source: ${source}`);
  }

  return response.json();
}

export async function getSourceCrawls(
  source: string,
  limit = 10,
): Promise<CrawlRun[]> {
  const response = await fetch(
    `${API_URL}/sources/${encodeURIComponent(source)}/crawls?limit=${limit}`,
    {
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch crawl history for source: ${source}`);
  }

  return response.json();
}
