import type { SourceHealth } from "@/types/source";

interface DashboardStatsProps {
  sources: SourceHealth[];
}

export function DashboardStats({ sources }: DashboardStatsProps) {
  const normalCount = sources.filter(
    (source) => source.health.toUpperCase() === "NORMAL",
  ).length;

  const warningCount = sources.filter(
    (source) => source.health.toUpperCase() === "WARNING",
  ).length;

  const failedCount = sources.filter(
    (source) => source.health.toUpperCase() === "FAILED",
  ).length;

  const stats = [
    {
      label: "Sources",
      value: sources.length,
    },
    {
      label: "Normal",
      value: normalCount,
    },
    {
      label: "Warning",
      value: warningCount,
    },
    {
      label: "Failed",
      value: failedCount,
    },
  ];

  return (
    <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="rounded-xl border bg-white p-5 shadow-sm"
        >
          <p className="text-sm text-gray-500">{stat.label}</p>

          <p className="mt-2 text-3xl font-bold">{stat.value}</p>
        </div>
      ))}
    </div>
  );
}
