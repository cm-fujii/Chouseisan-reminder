BUCKET_NAME := cm-fujii.genki-chouseisan-reminder-deploy-bucket
STACK_NAME := Chouseisan-Reminder-Stack
PARAMETER_STORE_KEY := /Slack/INCOMING_WEBHOOK_URL/misc-join-201901/message

build:
	sam build

deploy:
	sam package \
		--output-template-file packaged.yaml \
		--s3-bucket $(BUCKET_NAME)

	sam deploy \
		--template-file packaged.yaml \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_NAMED_IAM \
		--no-fail-on-empty-changeset \
		--parameter-overrides ChouseisanNotifySlackUrl=$(PARAMETER_STORE_KEY)

test:
	INCOMMING_WEBHOOK_URL=test_url python -m pytest tests/ -v

get-endpoint:
	aws cloudformation describe-stacks \
		--stack-name $(STACK_NAME) \
		--query 'Stacks[].Outputs'
