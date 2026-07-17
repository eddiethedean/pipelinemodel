document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;
  // Shipped in 0.5: DATAFRAME_PLUGINS, POLARS, PANDAS.
  // Shipped in 0.6: SQL, SQL_EXECUTION, SQL_PUSHDOWN.
  // Shipped in 0.7: PYSPARK, PYSPARK_EXECUTION, SPARK_OPTIMIZATION (batch).
  // Experimental in 0.7: STRUCTURED_STREAMING (separate experimental banner).
  const futureExecutionPages = [
    "PLUGINS",
    "ORCHESTRATION_PLUGINS",
    "STORAGE_PLUGINS",
    "RESOURCE_PLUGINS",
    "AIRFLOW",
    "COMPILATION",
  ];
  const experimentalExecutionPages = ["STRUCTURED_STREAMING"];
  const isFutureExecution = futureExecutionPages.some((name) =>
    path.includes(`/06_EXECUTION/${name}/`)
  );
  const isExperimentalExecution = experimentalExecutionPages.some((name) =>
    path.includes(`/06_EXECUTION/${name}/`)
  );
  // Dataframe, SQL, and Spark plugin protocols are shipped; other Plugin SDK pages are future.
  const isPluginSdk =
    path.includes("/07_PLUGIN_SDK/") &&
    !path.includes("/07_PLUGIN_SDK/DATAFRAME_PLUGIN/") &&
    !path.includes("/07_PLUGIN_SDK/SQL_PLUGIN/") &&
    !path.includes("/07_PLUGIN_SDK/SQL_DIALECT/") &&
    !path.includes("/07_PLUGIN_SDK/PYSPARK_PLUGIN/") &&
    !path.includes("/07_PLUGIN_SDK/SPARK_PROVIDER/");
  const isDesignExample =
    path.includes("/09_EXAMPLES/") && !path.endsWith("/09_EXAMPLES/");
  const isFutureVisualization =
    path.includes("/08_VISUALIZATION/") &&
    !path.endsWith("/08_VISUALIZATION/") &&
    !path.includes("/08_VISUALIZATION/MERMAID/") &&
    !path.includes("/08_VISUALIZATION/README");
  const isProposedReference =
    path.includes("/10_REFERENCE/CONFIGURATION/") ||
    path.includes("/10_REFERENCE/ENVIRONMENT_VARIABLES/");

  const article = document.querySelector("article.md-content__inner");
  if (!article) return;

  if (isExperimentalExecution) {
    const banner = document.createElement("div");
    banner.className = "admonition warning";
    banner.innerHTML =
      '<p class="admonition-title">Experimental in ETLantic 0.7</p>' +
      "<p>Structured Streaming APIs are experimental. Batch Spark via " +
      "<code>etlantic-pyspark</code> is the production path. See Current Capabilities.</p>";
    article.prepend(banner);
    return;
  }

  if (
    !isFutureExecution &&
    !isPluginSdk &&
    !isDesignExample &&
    !isFutureVisualization &&
    !isProposedReference
  ) {
    return;
  }

  const banner = document.createElement("div");
  banner.className = "admonition warning";
  banner.innerHTML =
    '<p class="admonition-title">Future design—not a ETLantic 0.7 API guide</p>' +
    "<p>This page may contain unshipped packages, commands, or interfaces. " +
    "Use Current Capabilities, the API reference, and the CLI reference for shipped behavior. " +
    "PySpark batch execution is available via <code>etlantic-pyspark</code>.</p>";
  article.prepend(banner);
});
