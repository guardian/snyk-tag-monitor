import "source-map-support/register";
import { App } from "aws-cdk-lib";
import { SnykTagMonitor } from "../lib/snyk-tag-monitor";

const app = new App();
new SnykTagMonitor(app, "SnykTagMonitor-PROD", { stack: "snyk-tag-monitor", stage: "PROD" });
