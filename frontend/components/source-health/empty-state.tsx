export function EmptyState() {
  return (
    <div className="mt-8 rounded-xl border bg-white p-10 text-center shadow-sm">
      <h2 className="text-xl font-semibold">No sources found</h2>

      <p className="mt-2 text-sm text-gray-500">
        No scraping sources have reported health data yet.
      </p>
    </div>
  );
}
