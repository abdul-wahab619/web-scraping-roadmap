export default function Loading() {
  return (
    <main className="min-h-screen bg-gray-50 px-6 py-10">
      <div className="mx-auto max-w-6xl">
        <div>
          <div className="h-9 w-64 animate-pulse rounded-lg bg-gray-200" />

          <div className="mt-3 h-5 w-96 animate-pulse rounded bg-gray-200" />
        </div>

        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, index) => (
            <div
              key={index}
              className="h-28 animate-pulse rounded-xl border bg-white"
            />
          ))}
        </div>

        <div className="mt-8 h-64 animate-pulse rounded-xl border bg-white" />

        <div className="mt-8 h-96 animate-pulse rounded-xl border bg-white" />
      </div>
    </main>
  );
}
