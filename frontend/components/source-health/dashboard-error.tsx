interface DashboardErrorProps {
  message: string;
}

export function DashboardError({ message }: DashboardErrorProps) {
  return (
    <div className="mt-8 rounded-xl border border-red-200 bg-red-50 p-6">
      <h2 className="text-lg font-semibold text-red-800">
        Unable to load source health
      </h2>

      <p className="mt-2 text-sm text-red-700">{message}</p>
    </div>
  );
}
