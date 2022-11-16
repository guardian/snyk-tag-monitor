import type { GuStackProps } from '@guardian/cdk/lib/constructs/core';
import { GuStack } from '@guardian/cdk/lib/constructs/core';
import type { GuScheduledLambdaProps } from '@guardian/cdk/lib/patterns';
import { GuScheduledLambda } from '@guardian/cdk/lib/patterns';
import type { App } from 'aws-cdk-lib';
import { Duration } from 'aws-cdk-lib';
import { Schedule } from 'aws-cdk-lib/aws-events';
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
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

		const snykApiKey = new Secret(this, 'snykApiKey');
		const snykGroupId = new Secret(this, 'snykGroupId');

		const lambdaProps: GuScheduledLambdaProps = {
			rules: [{ schedule: Schedule.rate(Duration.days(2)) }],
			monitoringConfiguration: {
				noMonitoring : true
			},
			runtime: Runtime.PYTHON_3_9,
			handler: 'main.handler',
			app,
			fileName: `${app}.zip`,
			environment: {
				SNYK_API_KEY_ARN: snykApiKey.secretArn,
				SNYK_GROUP_ID_ARN: snykGroupId.secretArn,
				SNS_TOPIC_ARN: topic.topicArn,
			},
		};

		const lambda = new GuScheduledLambda(this, app, lambdaProps);

		topic.grantPublish(lambda);
		snykApiKey.grantRead(lambda)
		snykGroupId.grantRead(lambda)
		
	}
}
