import type { GuStackProps } from "@guardian/cdk/lib/constructs/core";
import { GuStack } from "@guardian/cdk/lib/constructs/core";
import type {GuScheduledLambdaProps} from "@guardian/cdk/lib/patterns"
import {GuScheduledLambda} from "@guardian/cdk/lib/patterns"
import type { App} from "aws-cdk-lib";
import { Duration } from "aws-cdk-lib";
import { Schedule } from "aws-cdk-lib/aws-events";
import { Runtime } from "aws-cdk-lib/aws-lambda";
import {Secret} from "aws-cdk-lib/aws-secretsmanager"


export class SnykTagMonitor extends GuStack {
  constructor(scope: App, id: string, props: GuStackProps) {
    super(scope, id, props);

    const app = "snyk-tag-monitor"
    const lambdaProps: GuScheduledLambdaProps = {
      rules: [{ schedule: Schedule.rate(Duration.days(2))}],
      monitoringConfiguration: {
        toleratedErrorPercentage: 50,
        snsTopicName: "devx-alerts",
      },
      runtime: Runtime.PYTHON_3_9,
      handler: "lib/handler.handler",
      app,
      fileName: `${app}.zip` 
    }

    const snykTagLambda = new GuScheduledLambda(this,
      app, lambdaProps)

    const snykApiKey = new Secret(this, "snykApiKey")
    const snykGroupId = new Secret(this, "snykGroupId")

  }
}
