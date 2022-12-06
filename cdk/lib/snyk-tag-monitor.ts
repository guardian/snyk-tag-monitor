import { GuAlarm } from '@guardian/cdk/lib/constructs/cloudwatch';
import type { GuAlarmProps } from '@guardian/cdk/lib/constructs/cloudwatch';
import type { GuStackProps } from '@guardian/cdk/lib/constructs/core';
import { GuStack } from '@guardian/cdk/lib/constructs/core';
import type { GuScheduledLambdaProps } from '@guardian/cdk/lib/patterns';
import { GuScheduledLambda } from '@guardian/cdk/lib/patterns';
import type { App } from 'aws-cdk-lib';
import { Duration } from 'aws-cdk-lib';
import { ComparisonOperator, Metric } from 'aws-cdk-lib/aws-cloudwatch';
import type { MetricProps } from 'aws-cdk-lib/aws-cloudwatch';
import { Schedule } from 'aws-cdk-lib/aws-events';
import { PolicyStatement } from 'aws-cdk-lib/aws-iam';
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import { Topic } from 'aws-cdk-lib/aws-sns';
import { EmailSubscription } from 'aws-cdk-lib/aws-sns-subscriptions';

export class SnykTagMonitor extends GuStack {
	constructor(scope: App, id: string, props: GuStackProps) {
		super(scope, id, props);

		const app = 'snyk-tag-monitor';

		const topic = new Topic(this, `${app}-topic`);
		topic.addSubscription(
			new EmailSubscription('devx.security@guardian.co.uk'),
		);

        const metricProps: MetricProps = {
            namespace: 'snyk-tag-monitor',
            metricName: 'snykTagCount',
            dimensionsMap: {
                'stage': this.stage
            },
            period: Duration.days(1),
            statistic: "Minimum"
        }
        const tagMetric = new Metric(metricProps)

        const tagAlarmProps: GuAlarmProps = {
            comparisonOperator: ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold: 4500,
            evaluationPeriods: 1,
            snsTopicName: topic.topicName,
            metric: tagMetric,
            app: app,
            }
        const tagAlarm = new GuAlarm(this, `${app}-alarm`, tagAlarmProps)

		const lambdaProps: GuScheduledLambdaProps = {
			rules: [{ schedule: Schedule.rate(Duration.days(1)) }],
			monitoringConfiguration: {
				toleratedErrorPercentage: 50,
				snsTopicName: topic.topicName,
			},
			runtime: Runtime.PYTHON_3_9,
			handler: 'main.handler',
			app,
			fileName: `${app}.zip`,
			environment: {
				SNS_TOPIC_ARN: topic.topicArn,
			},
			timeout: Duration.minutes(5)
		};

		const lambda = new GuScheduledLambda(this, app, lambdaProps);
		topic.grantPublish(lambda);
        const policyStatement = new PolicyStatement({actions: ['cloudwatch:PutMetricData'], resources: ['*']})
        lambda.addToRolePolicy(policyStatement)
		
	}
}
