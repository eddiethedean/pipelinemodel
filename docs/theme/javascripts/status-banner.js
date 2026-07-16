document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;
  const futureExecutionPages = [
    "PLUGINS",
    "DATAFRAME_PLUGINS",
    "ORCHESTRATION_PLUGINS",
    "STORAGE_PLUGINS",
    "RESOURCE_PLUGINS",
    "POLARS",
    "PANDAS",
    "SQL",
    "SQL_EXECUTION",
    "SQL_PUSHDOWN",
    "PYSPARK",
    "PYSPARK_EXECUTION",
    "SPARK_OPTIMIZATION",
    "STRUCTURED_STREAMING",
    "AIRFLOW",
    "COMPILATION",
  ];
  const isFutureExecution = futureExecutionPages.some((name) =>
    path.includes(`/06_EXECUTION/${name}/`)
  );
  const isPluginSdk = path.includes("/07_PLUGIN_SDK/");
  const isDesignExample =
    path.includes("/09_EXAMPLES/") && !path.endsWith("/09_EXAMPLES/");

  if (!isFutureExecution && !isPluginSdk && !isDesignExample) return;

  const article = document.querySelector("article.md-content__inner");
  if (!article) return;

  const banner = document.createElement("div");
  banner.className = "admonition warning";
  banner.innerHTML =
    "<p class=\"admonition-title\">Future design—not a Pipelantic 0.4 API guide</p>" +
    "<p>This page may contain unshipped packages, commands, or interfaces. " +
    "Use Current Capabilities, the API reference, and the CLI reference for shipped behavior.</p>";
  article.prepend(banner);
});
