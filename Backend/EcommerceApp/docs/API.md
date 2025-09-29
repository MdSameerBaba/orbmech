# EcommerceApp API Documentation\n\n## Authentication Endpoints\n\n### POST /api/auth/register\nRegister new user\n\n**Request Body:**\n```json\n{
  "email": "string",
  "password": "string",
  "firstName": "string",
  "lastName": "string"
}\n```\n\n**Response:**\n```json\n{
  "user": "User",
  "token": "string"
}\n```\n\n### POST /api/auth/login\nLogin user\n\n**Request Body:**\n```json\n{
  "email": "string",
  "password": "string"
}\n```\n\n**Response:**\n```json\n{
  "user": "User",
  "token": "string"
}\n```\n\n### GET /api/auth/profile\nGet user profile\n\n**Response:**\n```json\n{
  "user": "User"
}\n```\n\n## API Endpoints\n\n### GET /api/products\nGet all products\n\n🔒 **Authentication Required**\n\n**Response:**\n```json\n{
  "products": "Array<Product>"
}\n```\n\n### POST /api/products\nCreate new product\n\n🔒 **Authentication Required**\n\n**Request Body:**\n```json\n{
  "name": "string",
  "description": "text",
  "price": "decimal",
  "stock": "integer",
  "category": "string",
  "imageUrl": "string",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}\n```\n\n**Response:**\n```json\n{
  "product": "Product"
}\n```\n\n### PUT /api/products/:id\nUpdate product\n\n🔒 **Authentication Required**\n\n**Request Body:**\n```json\n{
  "name": "string",
  "description": "text",
  "price": "decimal",
  "stock": "integer",
  "category": "string",
  "imageUrl": "string",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}\n```\n\n**Response:**\n```json\n{
  "product": "Product"
}\n```\n\n### DELETE /api/products/:id\nDelete product\n\n🔒 **Authentication Required**\n\n**Response:**\n```json\n{
  "message": "string"
}\n```\n\n### GET /api/orders\nGet all orders\n\n🔒 **Authentication Required**\n\n**Response:**\n```json\n{
  "orders": "Array<Order>"
}\n```\n\n### POST /api/orders\nCreate new order\n\n🔒 **Authentication Required**\n\n**Request Body:**\n```json\n{
  "userId": "string",
  "status": "string",
  "total": "decimal",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}\n```\n\n**Response:**\n```json\n{
  "order": "Order"
}\n```\n\n### PUT /api/orders/:id\nUpdate order\n\n🔒 **Authentication Required**\n\n**Request Body:**\n```json\n{
  "userId": "string",
  "status": "string",
  "total": "decimal",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}\n```\n\n**Response:**\n```json\n{
  "order": "Order"
}\n```\n\n### DELETE /api/orders/:id\nDelete order\n\n🔒 **Authentication Required**\n\n**Response:**\n```json\n{
  "message": "string"
}\n```\n\n