resource "aws_apigatewayv2_api" "root" {
  name          = "root-http-api"
  protocol_type = "HTTP"
  cors_configuration {
    allow_methods = ["*"]
    allow_headers = ["authorization"]
    expose_headers = ["date", "api-id"]
    allow_origins = ["*"] //change this
    allow_credentials = false
    max_age = 300
  }
}


resource "aws_apigatewayv2_integration" "get_route_integration" {
  api_id           = aws_apigatewayv2_api.root.id
  integration_type = "AWS_PROXY"
  connection_type           = "INTERNET"
  description               = "Lambda example"
  integration_uri           = aws_lambda_function.lambda_function.invoke_arn
  passthrough_behavior      = "WHEN_NO_MATCH"
} 

resource "aws_apigatewayv2_integration" "put_route_integration" {
  api_id           = aws_apigatewayv2_api.root.id
  integration_type = "AWS_PROXY"
  connection_type           = "INTERNET"
  description               = "Lambda example"
  integration_uri           = aws_lambda_function.lambda_function.invoke_arn
  passthrough_behavior      = "WHEN_NO_MATCH"
} 

resource "aws_apigatewayv2_route" "get_route" {
  api_id    = aws_apigatewayv2_api.root.id
  route_key = "GET /count"

  target = "integrations/${aws_apigatewayv2_integration.get_route_integration.id}"
}

resource "aws_apigatewayv2_route" "put_route" {
  api_id    = aws_apigatewayv2_api.root.id
  route_key = "PUT /count"

  target = "integrations/${aws_apigatewayv2_integration.get_route_integration.id}"
}

resource "aws_apigatewayv2_stage" "gateway_stage" {
  api_id = aws_apigatewayv2_api.root.id
  name   = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_deployment" "deploy" {
  api_id      = aws_apigatewayv2_api.root.id
  description = "Example deployment"

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [ 
    aws_apigatewayv2_route.get_route, 
    aws_apigatewayv2_route.put_route,
    aws_apigatewayv2_integration.get_route_integration,
    aws_apigatewayv2_integration.put_route_integration    
    ]
}

output "api_gateway_url" {
  value = aws_apigatewayv2_api.root.api_endpoint
}