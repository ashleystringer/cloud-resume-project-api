resource "aws_dynamodb_table" "visitor-count-table" {
  name           = "visitor-count-table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key = "id"

  attribute {
    name = "id"
    type = "S"
  }
}


resource "aws_dynamodb_table_item" "visitor-count-table-item" {
  table_name = aws_dynamodb_table.visitor-count-table.name
  hash_key   = aws_dynamodb_table.visitor-count-table.hash_key

  item = <<ITEM
{
  "id": {"S": "1"},
  "count": {"N": "0"}
}
ITEM
}