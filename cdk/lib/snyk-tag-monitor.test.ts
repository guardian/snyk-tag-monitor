import { App } from "aws-cdk-lib";
import { Template } from "aws-cdk-lib/assertions";
import { SnykTagMonitor } from "./snyk-tag-monitor";

describe("The SnykTagMonitor stack", () => {
  it("matches the snapshot", () => {
    const app = new App();
    const stack = new SnykTagMonitor(app, "SnykTagMonitor", { stack: "snyk-tag-monitor", stage: "TEST" });
    const template = Template.fromStack(stack);
    expect(template.toJSON()).toMatchSnapshot();
  });
});
