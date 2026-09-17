"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export function RefreshButton() {
  const router = useRouter();

  const [refreshing, setRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  useEffect(() => {
    setLastUpdated(new Date());
  }, []);

  async function handleRefresh() {
    setRefreshing(true);

    router.refresh();

    setLastUpdated(new Date());

    setTimeout(() => {
      setRefreshing(false);
    }, 500);
  }

  return (
    <div className="flex items-center gap-3">
      {lastUpdated && (
        <span className="text-xs text-gray-500">
          Updated {lastUpdated.toLocaleTimeString()}
        </span>
      )}

      <button
        type="button"
        onClick={handleRefresh}
        disabled={refreshing}
        className="rounded-lg border bg-white px-4 py-2 text-sm font-medium shadow-sm transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {refreshing ? "Refreshing..." : "Refresh"}
      </button>
    </div>
  );
}
