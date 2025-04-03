data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "archive_file" "lambda_package" {
  type = "zip"
  source_file = "lambda_function.py"
  output_path = "lambda_function.zip"
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_lambda_function" "lambda_function" {
  filename      = "lambda_function.zip"
  function_name = "visitor-counter-function"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.13"

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.visitor-count-table.name
    }
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role = aws_iam_role.iam_for_lambda.name
}

resource "aws_iam_role_policy_attachment" "lambda_microservice" {
  policy_arn = "arn:aws:iam::851725342515:policy/service-role/AWSLambdaMicroserviceExecutionRole-0432e8f8-6b31-4e03-87af-e019989c172e"
  role = aws_iam_role.iam_for_lambda.name
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_apigatewayv2_api.root.execution_arn}/*/*"
}
