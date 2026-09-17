export interface SourceHealth {
  source: string;
  latest_crawl_id: number;
  latest_status: string;

  latest_items_found: number;
  latest_items_dropped: number;

  latest_requests: number;
  latest_responses: number;
  latest_retries: number;
  latest_http_errors: number;
  latest_spider_exceptions: number;

  latest_duration: number | null;
  latest_finished_at: string | null;

  avg_items_found: number | null;
  percentage_of_average: number | null;

  health: string;

  last_successful_crawl: string | null;

  failed_crawls: number;
  consecutive_failures: number;

  latest_duration_seconds: number | null;
  avg_duration_seconds: number | null;
  duration_percentage_of_average: number | null;

  latest_error_message: string | null;
}
export interface CrawlRun {
  id: number;
  source: string;
  started_at: string;
  finished_at: string | null;

  status: string;
  items_found: number;
  items_dropped: number;

  requests: number;
  responses: number;
  retries: number;
  http_errors: number;
  spider_exceptions: number;

  error_message: string | null;
}
