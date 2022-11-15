import 'source-map-support/register';
import { GuRootExperimental } from '@guardian/cdk/lib/experimental/constructs/root';
import { SnykTagMonitor } from '../lib/snyk-tag-monitor';

const app = new GuRootExperimental();
new SnykTagMonitor(app, 'SnykTagMonitor-INFRA', {
	stack: 'security',
	stage: 'INFRA',
	env: { region: 'eu-west-1' },
});
